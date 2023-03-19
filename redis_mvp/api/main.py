from fastapi import FastAPI

from redis_mvp.queue.worker import start
from redis_mvp.queue.updater import Comment

app = FastAPI()


@app.post("/start")
async def start_job():
    """Kick off Redis Worker to retrieve and store data from API."""
    start()
    return {"status": "job started"}


@app.get("/comments")
async def get_comments():
    """Retrieve all comments from Redis DB."""
    return {"comments": Comment.find().all()}
