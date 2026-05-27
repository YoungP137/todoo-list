from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = 'postgresql+psycopg2://postgres:admin@pgdb:5432/postgres'
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker (bind = engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key = True, default = lambda : str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column (default= False)

class CategoriesORM(Base):
    __tablename__ = "categories"
    name: Mapped [str]
    

       
    
@asynccontextmanager
async def lifespan (_: FastAPI):
    Base.metadata.create_all (bind=engine)
    yield

priloj = FastAPI(lifespan=lifespan)


priloj.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"], 
    allow_methods=["*"],
    allow_headers =["*"],
    allow_credentials = True,
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
    

class CategoriesSchema(BaseModel):
    id: str
    name: str

class  CategoriesCreateSchema(BaseModel):
    name: str
    
class CategoriesUpdateSchema (BaseModel):
    name: str
  
    
book: list[BookCreate]= []


def get_db ():
    db = Sessionlocal()
    
    try:
        yield db
    finally:
        db.close()

def task_orm_to_module (task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id = task_orm.id, title = task_orm.title, completed = task_orm.completed)

def categories_orm_to_module (categories_orm: CategoriesORM) -> CategoriesSchema:
    return CategoriesSchema (id = categories_orm.id, name = categories_orm.name)

@priloj.get ("/tasks", response_model= list [TaskSchema])
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_module(task) for task in tasks_from_db]

@priloj.get ("/book", response_model= list[BookCreate])
def read_book():
    return f"Любимая книга: {book}"

@priloj.post("/tasks", response_model= TaskSchema, status_code= status.HTTP_201_CREATED)
def create_tasks(payload: TaskCreateSchema, db: Session = Depends(get_db)): 
    new_task = TaskORM( title=payload.title, completed = False)
    db.add (new_task)
    db.commit()
    return task_orm_to_module(new_task)

@priloj.post ("/book")
def create_book (payload: BookCreate):
    new_book  = payload.book
    book.append (new_book)
    return new_book

@priloj.patch("/tasks/{task_id}", response_model = TaskSchema, )
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed
        
    db.commit()
    return task_for_update


@priloj.delete("/tasks/{task_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()
        
@priloj.get('/categories', response_model = list [CategoriesSchema])
def read_categories (db: Session = Depends(get_db)) -> list[CategoriesSchema]:
    categories_from_db = db.scalars(select(CategoriesORM)).all()
    return [categories_orm_to_module(category) for category in categories_from_db]

@priloj.post('/categories', response_model = CategoriesSchema, status_code= status.HTTP_201_CREATED)
def create_categories (payload: CategoriesCreateSchema, db: Session = Depends(get_db)):
    new_categories = CategoriesORM (name = payload.name )
    db.add (new_categories)
    db.commit()
    return categories_orm_to_module(new_categories)

@priloj.patch('/categories/{categoriya_id}', response_model = CategoriesSchema)
def update_categories(categoriya_id: str, payload: CategoriesUpdateSchema, db: Session = Depends(get_db)) -> CategoriesSchema:
    categories_for_update = db.get(CategoriesORM, categoriya_id)
    if payload.name:
        categories_for_update.name = payload.name
    
    db.commit()
    return categories_for_update
    

    
@priloj.delete ('/categories/{categoriya_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_categories (categoriya_id, db: Session = Depends(get_db)) -> None:
    categories_for_delete = db.get(CategoriesORM, categoriya_id)
    db.delete(categories_for_delete)
    db.commit()
        
