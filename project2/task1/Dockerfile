FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tcpdump && rm -rf /var/lib/apt/lists/*

COPY server.py .
COPY client.py .

EXPOSE 5000