# P2P Network — CECS 327 Group Project 4

A distributed peer-to-peer network with file storage and key-value DHT routing, built with Python (Flask) and Docker.

---

## File Structure

```
project4/
├── app.py                # P2P node application (upload, download, KV store, DHT)
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Multi-node orchestration (node1, node2, node3)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Requirements

- Docker
- Docker Compose

---

## Quick Start

```bash
# Build images and start all 3 nodes
docker-compose up --build

# Or run in background
docker-compose up --build -d

# Stop and remove all containers
docker-compose down
```

---

## Manual Testing

### Phase 1 — File Upload & Download

```bash
# Upload a file to node1
echo "hello world" > test.txt
curl -F 'file=@test.txt' http://localhost:5001/upload

# Download the file from node1
curl http://localhost:5001/download/test.txt -o downloaded.txt
cat downloaded.txt
```

### Phase 2 & 3 — Key-Value Store with DHT Routing

```bash
# Store a key-value pair (DHT will route to responsible node automatically)
curl -X POST http://localhost:5001/kv \
  -H "Content-Type: application/json" \
  -d '{"key": "color", "value": "blue"}'

# Retrieve the value (works from any node — DHT forwards if needed)
curl http://localhost:5001/kv/color
curl http://localhost:5002/kv/color
curl http://localhost:5003/kv/color
```

### Health Check

```bash
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

---

## How It Works

1. **Three nodes** (node1, node2, node3) each run an identical Flask app inside Docker containers connected on a shared network.
2. **Phase 1 — File Storage:** Each node has a local `storage/` directory mounted as a Docker volume. Files uploaded to a node persist and can be downloaded directly from that node.
3. **Phase 2 — Key-Value Store:** Each node maintains an in-memory dictionary for storing key-value pairs via POST `/kv` and retrieving them via GET `/kv/<key>`.
4. **Phase 3 — DHT Routing:** When a key-value request arrives, the node computes a SHA-1 hash of the key and uses modulo arithmetic over the sorted node list to determine which node is responsible. If the current node is not responsible, it transparently forwards the request to the correct node and returns the response.
