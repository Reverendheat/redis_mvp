from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from redis_mvp.queue.worker import start
from redis_mvp.queue.updater import Comment


app = FastAPI()

templates = Jinja2Templates(directory='./redis_mvp/api/templates')


@app.post("/start")
async def start_job():
    """Kick off Redis Worker to retrieve and store data from API."""
    start()
    return {"status": "job started"}


@app.get("/api/comments")
async def get_json_comments():
    comments =  Comment.find().all()
    return {"comments": comments}


@app.get("/comments", response_class=HTMLResponse)
async def get_comments(request: Request):
    """Retrieve all comments from Redis DB."""
    comments =  Comment.find().all()
    return templates.TemplateResponse("comments.html", {"request": request, "comments": comments}) 
