FROM python:3.11.2-slim-bullseye as python-base


ENV LOCAL_SITE_PACKAGES="/opt/python" \
  \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100
ENV PYTHONPATH=".:${LOCAL_SITE_PACKAGES}" \
  PATH="${PATH}:${LOCAL_SITE_PACKAGES}}/bin"

FROM python-base as builder
RUN apt-get update || true && \
  apt-get install --no-install-recommends -y \
  curl \
  build-essential

ENV POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_NO_INTERACTION=1 \
  POETRY_PREVIEW=1

ENV PATH="${PATH}:${POETRY_HOME}/bin"
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM builder as dev
WORKDIR /src
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry export --without-hashes -o requirements.txt \
  && pip install -t ${LOCAL_SITE_PACKAGES} -r requirements.txt
WORKDIR /app
COPY ./redis_mvp /app/redis_mvp
ENTRYPOINT [ "python", "-u", "/app/redis_mvp/entrypoints/main.py" ]