FROM python:3.11-slim AS builder

WORKDIR /FastAPI_games

ENV PYTHONDONTWRITEBYTECODE = 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-ansi

FROM python:3.11-slim

WORKDIR /FastAPI_games

RUN apt-get update && apt-get install -y \
    postgresql-client\
    libpq5\
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /FastAPI_games/.venv /FastAPI_games/.venv

COPY . .

COPY /.env_container /FastAPI_games/.env

RUN mv .env_container .env

ENV PATH="/FastAPI_games/.venv/bin:$PATH"

EXPOSE 8000

RUN chmod +x ./src/scripts/start.sh
