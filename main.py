
from fastapi import Depends, FastAPI,status,HTTPException
from database import Base, engine,SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from typing import List

app=FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return "todos"


@app.post("/todo",response_model=schemas.Todos,status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate,session:Session=Depends(get_db)):
    session=Session(bind=engine,expire_on_commit=False)
    todos=models.Todos(title=todo.title)
    session.add(todos)
    session.commit()
    session.refresh(todos)
    session.close()
    return todos.db


@app.get("/todo/{id}",response_model=schemas.Todos)
def read_data(id:int):
    session=Session(bind=engine,expire_on_commit=False)
    todo=session.query(models.Todos).get(id)
    session.close()
    if not todos:
        raise HTTPException(status_code=404,detail=f"todo item with {id} not found")
    return todos
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


# @app.get("/todo/{todo_id}")
# async def read_todo(todo_id:int,db:Session = Depends(get_db)):
#     todo_model = db.query(models.Todos)\
#         .filter(models.Todos.id == todo_id)\
#         .first()
#     if todo_model is not None:
#         return todo_model
#     raise http_exception()

# def http_exception():
#     return HTTPConnection(status_code=404,details ="Todo not found")
