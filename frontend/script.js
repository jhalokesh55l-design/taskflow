const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const dueDateInput = document.getElementById("due-date");
const taskList = document.getElementById("task-list");
const titleError = document.getElementById("title-error");

let tasks = [];


function saveTasksToCache() {
    localStorage.setItem("taskflow_tasks", JSON.stringify(tasks));
}


function renderTasks() {
    taskList.innerHTML = "";

    if (tasks.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "No tasks found.";
        taskList.appendChild(emptyMessage);
        return;
    }

    tasks.forEach((task) => {
        const taskItem = document.createElement("article");
        taskItem.className = "task-item";

        const title = document.createElement("h3");
        title.textContent = task.title;

        const priority = document.createElement("p");
        priority.textContent = `Priority: ${task.priority}`;

        const dueDate = document.createElement("p");
        dueDate.textContent = `Due date: ${task.due_date || "Not set"}`;

        const status = document.createElement("p");
        status.textContent = `Status: ${task.status}`;

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";

        editButton.addEventListener("click", () => {
            editTask(task);
        });

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-btn";

        deleteButton.addEventListener("click", () => {
            deleteTask(task.id);
        });

        actions.appendChild(editButton);
        actions.appendChild(deleteButton);

        taskItem.appendChild(title);
        taskItem.appendChild(priority);
        taskItem.appendChild(dueDate);
        taskItem.appendChild(status);
        taskItem.appendChild(actions);

        taskList.appendChild(taskItem);
    });
}


async function loadTasks() {
    const cachedTasks = localStorage.getItem("taskflow_tasks");

    if (cachedTasks) {
        tasks = JSON.parse(cachedTasks);
        renderTasks();
    }

    try {
        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        tasks = await response.json();

        saveTasksToCache();
        renderTasks();
    } catch (error) {
        console.error("Error loading tasks:", error);
    }
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = titleInput.value.trim();

    if (!title) {
        titleError.textContent = "Task title cannot be empty.";
        return;
    }

    titleError.textContent = "";

    const newTask = {
        title: title,
        priority: priorityInput.value,
        due_date: dueDateInput.value.trim() || null,
        status: "todo",
        project_id: 1
    };

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newTask)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to create task");
        }

        const createdTask = await response.json();

        tasks.push(createdTask);
        saveTasksToCache();
        renderTasks();

        form.reset();
        priorityInput.value = "medium";

    } catch (error) {
        console.error("Error creating task:", error);
        alert(error.message);
    }
});


async function editTask(task) {
    const newTitle = prompt("Enter new task title:", task.title);

    if (newTitle === null) {
        return;
    }

    const trimmedTitle = newTitle.trim();

    if (!trimmedTitle) {
        alert("Task title cannot be empty.");
        return;
    }

    const updatedTask = {
        title: trimmedTitle,
        priority: task.priority,
        due_date: task.due_date,
        status: task.status
    };

    try {
        const response = await fetch(`${API_URL}/tasks/${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedTask)
        });

        if (!response.ok) {
            throw new Error("Failed to update task");
        }

        const savedTask = await response.json();

        tasks = tasks.map((item) => {
            if (item.id === task.id) {
                return savedTask;
            }

            return item;
        });

        saveTasksToCache();
        renderTasks();

    } catch (error) {
        console.error("Error updating task:", error);
        alert(error.message);
    }
}


async function deleteTask(taskId) {
    const confirmed = confirm("Delete this task?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Failed to delete task");
        }

        tasks = tasks.filter((task) => task.id !== taskId);

        saveTasksToCache();
        renderTasks();

    } catch (error) {
        console.error("Error deleting task:", error);
        alert(error.message);
    }
}


titleInput.addEventListener("input", () => {
    if (titleInput.value.trim()) {
        titleError.textContent = "";
    }
});


loadTasks();