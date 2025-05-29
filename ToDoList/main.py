from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq


class AddTask(BaseModel):
    tg_id: int
    title: str


class CompletedTask(BaseModel):
    id: int


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print('All good')
    yield

app = FastAPI(title="To Do List", lifespan=lifespan) 


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)


@app.get("/api/tasks/{tg_id}")
async def get_tasks(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_tasks(user.id)


@app.get("/api/profile/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    count_completed_tasks = await rq.count_comleted_tasks(user.id)

    return {'Выполнено заданий:': count_completed_tasks}


@app.post("/api/add")
async def add_task(task: AddTask):
    user = await rq.add_user(task.tg_id)
    await rq.add_tasks(user.id, task.title)
    return {'status': '200 OK'}


@app.patch("/api/completed")
async def completed_task(task: CompletedTask):
    await rq.update_task(task.id)
    return {'status': '200 OK'}