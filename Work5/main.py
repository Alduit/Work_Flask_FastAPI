from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

#uvicorn Work5.main:app --reload для запуска
app = FastAPI()
templates = Jinja2Templates(directory="./Work5/templates")


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


tasks = []
current_id = 1


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/tasks", response_model=List[Task])
def read_tasks():
    return tasks


@app.get("/tasks/{id}", response_model=Task)
def read_task(id: int):
    task = next((task for task in tasks if task["id"] == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global current_id
    new_task = {
        "id": current_id,
        **task.dict()
    }
    tasks.append(new_task)
    current_id += 1
    return new_task


@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, updated_task: TaskCreate):
    task = next((task for task in tasks if task["id"] == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.update(updated_task.dict())
    return task


@app.delete("/tasks/{id}", response_model=Task)
def delete_task(id: int):
    global tasks
    task = next((task for task in tasks if task["id"] == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks = [task for task in tasks if task["id"] != id]
    return task