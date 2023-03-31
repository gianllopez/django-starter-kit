# syntax=docker/dockerfile:1
FROM python:3.11.0-slim
WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt requirements.txt
RUN \
  apt update && \
  apt install libpq-dev gcc -y && \
  pip install -r requirements.txt
COPY . .