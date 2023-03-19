from redis_om import redis, Migrator
from rq.worker import RoundRobinWorker
from rq import Queue

from redis_mvp.common.constants import REDIS_OM_URL
from redis_mvp.queue.updater import update_comments

conn = redis.Redis(decode_responses=True).from_url(REDIS_OM_URL)

def start():
    """Add update_comments to default Queue."""
    q = Queue(connection=conn)
    q.enqueue(update_comments)

def init_worker():
    """Initialize Redis Worker to proccess queue entries."""
    conn.flushall() # Remove any existing keys / workers / queues
    Migrator().run() # Initialize JsonModel indexes

    worker = RoundRobinWorker(queues=Queue(connection=conn), connection=conn)
    start()
    worker.work()
