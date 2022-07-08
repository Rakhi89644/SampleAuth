from xmlrpc.client import Boolean
from pydantic import BaseModel
class ToDoCreate(BaseModel):
    title=str

class Todos(BaseModel):
    id = int
    title = str
    description = str
   
    class Config:
        orm_mode=True