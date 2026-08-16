from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import User, Project, Task

app = FastAPI(title="TaskFlow API")


class UserCreate(BaseModel):
    name: str
    email: str


class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class TaskCreate(BaseModel):
    title: str
    priority: str
    due_date: str | None = None
    status: str = "todo"
    project_id: int


@app.get("/")
def home():
    return {"message": "TaskFlow API is running"}


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/projects")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    owner = db.get(User, project.owner_id)

    if not owner:
        raise HTTPException(status_code=404, detail="User not found")

    new_project = Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    project = db.get(Project, task.project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if task.priority not in ["low", "medium", "high"]:
        raise HTTPException(
            status_code=400,
            detail="Priority must be low, medium, or high"
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


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()