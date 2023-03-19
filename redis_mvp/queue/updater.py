from typing import Any
from datetime import datetime

import httpx
from redis_om import JsonModel, Field, NotFoundError

from redis_mvp.common.constants import COMMENT_TTL, COMMENT_BASE_URL

class Comment(JsonModel):
    name: str = Field(index=True)
    postId: int = Field(index=True)
    id: int = Field(index=True)
    email: str
    body: str
    last_seen: str

http_client = httpx.Client(base_url=COMMENT_BASE_URL, headers={"Accept": "application/json"})

def _update_timestamp(comments: list[dict[str,Any]]) -> list[dict[str, Any]]:
    """Add last_seen key with current timestamp."""
    time_now = datetime.now().isoformat()
    for comment in comments:
       comment['last_seen'] = time_now
    return comments

def fetch_comments() -> list[dict[str,Any]]:
    """Retrieve all comment data from API."""
    response = http_client.get("/comments")
    comments = response.json()
    return comments


def update_comments():
    """Fetch comments and add to database."""
    comments = fetch_comments()
    updated_comments = _update_timestamp(comments)
    for comment in updated_comments:
        try:
          existing_user = Comment.find(Comment.name == comment['name']).first()
          existing_user.update(**comment)
          existing_user.expire(int(COMMENT_TTL))
        except NotFoundError:
          co = Comment(**comment)
          co.save()
          co.expire(int(COMMENT_TTL))


