from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

categor = FastAPI()
categor.add_middleware (
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
)

categories: list[CategoriesSchema] = []

class CategoriesSchema(BaseModel):
    id: str
    name: str

class  CategoriesCreateSchema(BaseModel):
    name: str
    
class CategoroiesUpdateSchema (BaseModel):
    name: str

@categor.get('/categories')
def read_categories () -> list[CategoriesSchema]:
    return categories

@categor.post('/categories', status_code= status.HTTP_201_CREATED)
def create_categories (payload: CategoriesCreateSchema):
    new_categories = CategoriesSchema (id= str(uuid4()), name = payload.name )
    categories.append(new_categories)
    return new_categories

@categor.patch('/categories/{categoriya_id}')
def update_categories(categoriya_id: str, payload: CategoroiesUpdateSchema):
    for categoriya in categories:
        if categoriya.id == categoriya_id:
            categoriya.name = payload.name if payload.name else categoriya.name
        return categoriya
    
@categor.delete ('/categories/{categoriya_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_categories (categoriya_id):
    for categoriya in categories:
        if categoriya.id == categoriya_id:
            categories.remove(categoriya)
    