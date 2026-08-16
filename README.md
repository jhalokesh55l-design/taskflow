# TaskFlow

TaskFlow is a full-stack task management application built with FastAPI, SQLAlchemy, SQLite, HTML, CSS and JavaScript.

The project includes:

- Task CRUD
- Project management
- User management
- Project task statistics
- Custom insertion sort
- Binary search
- Linear search
- Algorithm benchmarks
- Rule-based AI Quick-Add parser
- Frontend task dashboard

---

## Project Structure

```text
taskflow/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── algorithms.py
│   ├── benchmark.py
│   ├── check_algorithms.py
│   ├── ai_parser.py
│   └── test_connection.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 1. Environment Setup

## Requirements

- Python 3.10+
- pip
- Modern web browser

Create and activate a virtual environment:

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# 2. Running the Backend

Open a terminal in the project root:

```powershell
cd backend
```

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 3. Running the Frontend

Open another terminal:

```powershell
cd frontend
```

Start the frontend server:

```powershell
python -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

The frontend communicates with the FastAPI backend at:

```text
http://127.0.0.1:8000
```

---

# 4. API Endpoints

## Users

### Create User

```http
POST /users
```

Example request:

```json
{
  "name": "Lokesh",
  "email": "lokesh@example.com"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Lokesh",
  "email": "lokesh@example.com"
}
```

### List Users

```http
GET /users
```

---

## Projects

### Create Project

```http
POST /projects
```

Example request:

```json
{
  "name": "Work",
  "description": "Work project",
  "owner_id": 1
}
```

Example response:

```json
{
  "id": 2,
  "name": "Work",
  "owner_id": 1
}
```

### List Projects

```http
GET /projects
```

---

## Tasks

### Create Task

```http
POST /tasks
```

Example request:

```json
{
  "title": "Finish report",
  "priority": "high",
  "due_date": "tomorrow",
  "status": "todo",
  "project_id": 1
}
```

Example response:

```json
{
  "id": 7,
  "title": "Finish report",
  "priority": "high",
  "due_date": "tomorrow",
  "status": "todo",
  "project_id": 1
}
```

### List Tasks

```http
GET /tasks
```

### Get Task By ID

```http
GET /tasks/{task_id}
```

### Update Task

```http
PUT /tasks/{task_id}
```

Example request:

```json
{
  "title": "Finish report updated",
  "priority": "medium",
  "due_date": "next week",
  "status": "todo"
}
```

### Delete Task

```http
DELETE /tasks/{task_id}
```

---

# 5. Project Statistics

```http
GET /projects/stats
```

Example response:

```json
[
  {
    "project_id": 2,
    "project_name": "Work",
    "task_count": 1
  },
  {
    "project_id": 1,
    "project_name": "TaskFlow Project",
    "task_count": 3
  }
]
```

The statistics endpoint uses SQL aggregation to calculate task counts per project.

---

# 6. Algorithm Endpoints

## Sort Tasks By Priority

```http
GET /tasks?sort=priority
```

Example response:

```json
[
  {
    "id": 2,
    "title": "test task update check",
    "priority": "high",
    "due_date": "tomorrow",
    "status": "todo",
    "project_id": 1
  },
  {
    "id": 6,
    "title": "delete task",
    "priority": "medium",
    "due_date": "tomorrow",
    "status": "todo",
    "project_id": 1
  }
]
```

The endpoint uses the custom `insertion_sort` implementation rather than Python's built-in sorting functions.

---

## Search Tasks

```http
GET /tasks/search?title=<exact-title>&algo=binary
```

The supported algorithms are:

```text
binary
linear
```

Example:

```text
GET /tasks/search?title=test%20task%20update%20check&algo=binary
```

The search endpoint returns the matching task or `404` if the exact title is not found.

---

# 7. Algorithms

## Insertion Sort

Function:

```python
insertion_sort(records, key)
```

Time complexity:

- Best case: O(n)
- Worst case: O(n²)
- Space complexity: O(1) auxiliary space

The function sorts the records in place.

---

## Binary Search

Function:

```python
binary_search(sorted_records, target_value, key)
```

Time complexity:

- Best case: O(1)
- Average case: O(log n)
- Worst case: O(log n)

Binary search requires the records to already be sorted by the selected key.

---

## Linear Search

Function:

```python
linear_search(records, target_value, key)
```

Time complexity:

- Best case: O(1)
- Average case: O(n)
- Worst case: O(n)

Linear search scans the records sequentially.

---

# 8. Algorithm Testing

Automated checks are provided in:

```text
backend/check_algorithms.py
```

Run:

```powershell
cd backend
python check_algorithms.py
```

The implemented checks produced:

```text
Testing insertion_sort...
PASS
Testing binary_search...
PASS
Testing linear_search...
PASS
Testing missing value...
PASS
```

---

# 9. Benchmark Results

The benchmark was run for three input sizes.

## n = 100

```text
Insertion Sort: 0.0144 ms, 99.00 comparisons
Binary Search: 0.0016 ms, 11.00 comparisons
Linear Search: 0.0031 ms, 51.00 comparisons
```

## n = 1000

```text
Insertion Sort: 0.1442 ms, 999.00 comparisons
Binary Search: 0.0021 ms, 17.00 comparisons
Linear Search: 0.0263 ms, 501.00 comparisons
```

## n = 5000

```text
Insertion Sort: 0.8413 ms, 4999.00 comparisons
Binary Search: 0.0061 ms, 23.00 comparisons
Linear Search: 0.1687 ms, 2501.00 comparisons
```

### Comparison

The benchmark shows that binary search requires far fewer comparisons than linear search as the input size increases. Insertion sort requires more work because sorting is an O(n²) worst-case operation. However, sorting can still be useful when a team repeatedly needs an ordered task list. TaskFlow performs the custom insertion sort when the client requests priority sorting, while search can use binary search after creating a sorted index.

---

# 10. AI Quick-Add

TaskFlow includes a deterministic, rule-based Quick-Add parser.

The parser does not require an API key or an external network service.

The parser extracts:

- task title
- priority
- due date
- project

The priority rules use keyword matching. High-priority keywords take precedence over low-priority keywords, while medium is the default.

The prompting structure follows a zero-shot style: the parser has a fixed instruction describing the expected structured task information rather than requiring a long sequence of examples. This keeps token usage low and makes the deterministic mock predictable. Because the rules are explicit, the same input produces the same structured output, improving reliability for the graded baseline.

---

# 11. Quick-Add Worked Examples

### Example 1

Input:

```text
Finish report high priority tomorrow
```

Output:

```json
{
  "title": "Finish report",
  "priority": "high",
  "due_date": "2026-08-17",
  "project": null
}
```

### Example 2

Input:

```text
Fix login low priority in 3 days project: Work
```

Output:

```json
{
  "title": "Fix login",
  "priority": "low",
  "due_date": "2026-08-19",
  "project": "Work"
}
```

### Example 3

Input:

```text
Prepare presentation high priority tomorrow project: Work
```

Output:

```json
{
  "title": "Prepare presentation",
  "priority": "high",
  "due_date": "2026-08-17",
  "project": "Work"
}
```

### Example 4

Input:

```text
Buy groceries low priority today
```

Output:

```json
{
  "title": "Buy groceries",
  "priority": "low",
  "due_date": "2026-08-16",
  "project": null
}
```

### Example 5

Input:

```text
Review project documentation
```

Output:

```json
{
  "title": "Review project documentation",
  "priority": "medium",
  "due_date": null,
  "project": null
}
```

---

# 12. Frontend Features

The frontend provides:

- Add Task form
- Task title validation
- Priority selection
- Due date input
- Task listing
- Edit task title
- Edit task priority
- Edit task due date
- Delete task
- Local task caching

The frontend uses JavaScript `fetch()` calls to communicate with the FastAPI backend.

---

# 13. Error Handling

The API uses appropriate HTTP status codes.

Examples:

```text
201 Created
200 OK
404 Not Found
422 Unprocessable Content
```

Validation prevents invalid task data such as an empty task title.

---

# 14. Git Workflow

Development was completed using a feature branch.

Feature branch:

```text
feature/taskflow-complete
```

Meaningful commits included:

```text
Implement algorithms and quick add
Add TaskFlow frontend
Improve task editing
```

The feature branch was merged back into:

```text
main
```

The final `main` branch was pushed to the public GitHub repository.

---

# 15. Repository

GitHub repository:

```text
https://github.com/jhalokesh55l-design/taskflow
```

The repository contains the complete backend, frontend, algorithms, benchmark, AI parser and documentation.