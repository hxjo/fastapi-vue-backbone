FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential libssl-dev libffi-dev git openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /srv

COPY fastapi/pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY fastapi/alembic.ini ./
COPY fastapi/alembic ./alembic/

EXPOSE 8000
