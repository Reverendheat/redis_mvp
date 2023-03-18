import sys

import uvicorn

from redis_mvp.api.main import app
from redis_mvp.common.constants import SERVER_ADDRESS, SERVER_PORT
from redis_mvp.common.exceptions import ArgumentError
from redis_mvp.redis_worker.worker import init_worker

if __name__ == "__main__":
    if not sys.argv[1]:
        raise ArgumentError("Missing required argument: command")
    if sys.argv[1] == "api":
        uvicorn.run(app, host=SERVER_ADDRESS, port=int(SERVER_PORT))
    elif sys.argv[1] == "worker":
        init_worker()
    else:
        raise ArgumentError(f"{sys.argv[1]} is not a supported command.")
