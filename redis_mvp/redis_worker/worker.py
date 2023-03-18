from redis_om import redis, Migrator
from rq.worker import RoundRobinWorker
from rq import Queue

from redis_mvp.common.constants import REDIS_OM_URL
from redis_mvp.redis_worker.updater import update_comments

conn = redis.Redis(decode_responses=True).from_url(REDIS_OM_URL)

def start():
    q = Queue(connection=conn)
    q.enqueue(update_comments)

def init_worker():
    conn.flushall() # Remove any existing keys / workers / queues
    Migrator().run() # Initialize JsonModel indexes

    worker = RoundRobinWorker(queues=Queue(connection=conn), connection=conn)
    start()
    worker.work()
