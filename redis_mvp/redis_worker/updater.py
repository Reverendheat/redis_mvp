import httpx
from datetime import datetime
from redis_om import JsonModel, Field, NotFoundError

from redis_mvp.common.constants import COMMENT_TTL, COMMENT_BASE_URL

class Comment(JsonModel):
    name: str = Field(index=True)
    postId: int = Field(index=True)
    email: str
    body: str
    last_seen: str

http_client = httpx.Client(base_url=COMMENT_BASE_URL, headers={"Accept": "application/json"})

def fetch_comments():
    time_now = datetime.now().isoformat()
    response = http_client.get("/comments")

    comments = response.json()
    for comment in comments:
       comment['last_seen'] = time_now
    return comments

def update_comments():
    comments = fetch_comments()
    for comments in comments:
        try:
          existing_user = Comment.find(Comment.name == comments['name']).first()
          existing_user.update(**comments)
          existing_user.expire(int(COMMENT_TTL))
        except NotFoundError:
          u = Comment(**comments)
          u.save()
          u.expire(int(COMMENT_TTL))


