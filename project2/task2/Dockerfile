FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tcpdump && rm -rf /var/lib/apt/lists/*

COPY multicast_sender.py .
COPY multicast_receiver.py .