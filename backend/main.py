from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, Field, field_validator
import time
from ai_parser import parse_quick_add
from database import get_db
from models import User, Project, Task
from algorithms import insertion_sort, binary_search, linear_search


app = FastAPI(title="TaskFlow API")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


# Request timing middleware
@app.middleware("http")
async def request_timer(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {elapsed_ms:.2f} ms"
    )

    return response


# -------------------------
# Pydantic models
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str


class ProjectCreate(BaseModel):
    name: str
    owner_id: int
class QuickAddRequest(BaseModel):
    description: str
    project_id: int

class TaskCreate(BaseModel):
    title: str
    priority: str = Field(
        ...,
        pattern="^(low|medium|high)$"
    )
    due_date: str | None = None
    status: str = "todo"
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


class TaskUpdate(BaseModel):
    title: str
    priority: str = Field(
        ...,
        pattern="^(low|medium|high)$"
    )
    due_date: str | None = None
    status: str = "todo"

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {"message": "TaskFlow API is running"}


# -------------------------
# USERS
# -------------------------

@app.post("/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# -------------------------
# PROJECTS
# -------------------------

@app.post("/projects", status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    owner = db.get(User, project.owner_id)

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_project = Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


# -------------------------
# TASKS
# -------------------------

@app.post("/tasks", status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    project = db.get(Project, task.project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        status=task.status,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
@app.post("/tasks/quick-add", status_code=201)
def quick_add_task(
    request: QuickAddRequest,
    db: Session = Depends(get_db)
):
    try:
        parsed = parse_quick_add(request.description)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    project_id = request.project_id

    if parsed["project"]:
        project = (
            db.query(Project)
            .filter(Project.name == parsed["project"])
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        project_id = project.id

    project = db.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = Task(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date"],
        status="todo",
        project_id=project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
@app.get("/tasks")
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    records = [
        {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "due_date": task.due_date,
            "status": task.status,
            "project_id": task.project_id
        }
        for task in tasks
    ]

    if sort == "priority":
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        for record in records:
            record["priority_rank"] = priority_order.get(
                record["priority"],
                99
            )

        insertion_sort(records, "priority_rank")

        for record in records:
            del record["priority_rank"]

    return records

@app.get("/tasks/search")
def search_tasks(
    title: str = Query(...),
    algo: str = Query(...),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    records = [
        {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "due_date": task.due_date,
            "status": task.status,
            "project_id": task.project_id
        }
        for task in tasks
    ]

    if algo == "linear":
        index = linear_search(records, title, "title")

    elif algo == "binary":
        insertion_sort(records, "title")
        index = binary_search(records, title, "title")

    else:
        raise HTTPException(
            status_code=400,
            detail="algo must be binary or linear"
        )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return records[index]

@app.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = task_data.title
    task.priority = task_data.priority
    task.due_date = task_data.due_date
    task.status = task_data.status

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# -------------------------
# PROJECT STATISTICS
# -------------------------

@app.get("/projects/stats")
def project_statistics(db: Session = Depends(get_db)):
    results = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
            func.count(Task.id).label("task_count")
        )
        .outerjoin(Task, Project.id == Task.project_id)
        .group_by(Project.id, Project.name)
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "task_count": row.task_count
        }
        for row in results
    ]