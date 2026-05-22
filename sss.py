from uuid import uuid4
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


priloj = FastAPI()


priloj.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3006"], 
    allow_methods=["*"],
)   


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool
    
class TaskCreateSchema(BaseModel):
    title: str
    
class BookCreate(BaseModel):
    book: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
    
    

tasks: list[TaskSchema] = []
book: list[BookCreate]= []


@priloj.get ("/tasks")
def read_tasks() -> list[TaskSchema]:
    return tasks

@priloj.get ("/book")
def read_book():
    return f"Любимая книга: {book}"

@priloj.post("/tasks", status_code= status.HTTP_201_CREATED)
def create_tasks(payload: TaskCreateSchema): 
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed = False)
    tasks.append(new_task)
    return new_task

@priloj.post ("/book")
def create_book (payload: BookCreate):
    new_book  = payload.book
    book.append (new_book)
    return new_book

@priloj.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title is None:
                task.title = payload.title
            if payload.completed is not None: 
                task.completed = payload.completed
            
            return task
        
@priloj.delete("/tasks/{task_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            
            
