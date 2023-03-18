import os

# Set from docker-compose.yml

# FASTAPI
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "")
SERVER_PORT = os.getenv("SERVER_PORT", 8000)

# REDIS
COMMENT_TTL = os.getenv("COMMENT_TTL", 3600)
COMMENT_BASE_URL = os.getenv("COMMENT_BASE_URL", "https://jsonplaceholder.typicode.com")
REDIS_OM_URL = os.getenv("REDIS_OM_URL", "redis://redis:6379")

