from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq


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