from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")


app = FastAPI(lifespan=lifespan)


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


@app.get("/")
async def home():
    return {"data": "Hello World"}


@app.post("/")
async def add_task(task: STaskAdd = Depends()):
    return {"data": task}


# uvicorn main:app --reload