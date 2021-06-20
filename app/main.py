from app.model import db_session, Todo, to_dict
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

### Start App ###
app = FastAPI()

### Start Session ###
db = db_session.session_factory()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/todos")
async def get_todos():
    q = db.query(Todo)
    todos = [to_dict(qq) for qq in q]
    return todos


class Data(BaseModel):
    title: str
    description: str


@app.post("/todos")
async def post_todos(data: Data):
    todo = Todo(title=data.title, description=data.description)
    try:
        db.add(todo)
        db.commit()
        db.refresh(todo)
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Cannot Create Todo")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="created!")
