from fastapi import FastAPI

from redis_mvp.redis_worker.worker import start
from redis_mvp.redis_worker.updater import Comment

app = FastAPI()


@app.post("/start")
async def start_job():
    start()
    return {"status": "job started"}


@app.get("/comments")
async def get_comments():
    return {"comments": Comment.find().all()}
