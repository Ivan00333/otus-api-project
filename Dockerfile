FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

COPY . .