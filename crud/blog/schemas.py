from fastapi.param_functions import Body
from pydantic import BaseModel
from sqlalchemy import orm


class Blog(BaseModel):
    title:str
    body:str

class ShowBlog(BaseModel):
    title:str
    body:str
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str