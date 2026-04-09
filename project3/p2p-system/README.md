# P2P Network — CECS 327 Group Project 3

A peer-to-peer network built with Python (Flask) and Docker.

---

## File Structure

```
p2p-system/
├── node.py               # P2P node application
├── bootstrap.py          # Bootstrap registry node
├── Dockerfile            # Image for p2p-node
├── bootstrap.Dockerfile  # Image for bootstrap-node
├── requirements.txt      # Python dependencies
├── Makefile              # Build / run / test helpers
└── README.md
```

---

## Requirements

- Docker
- Docker Compose (optional)
- `make` (or run commands manually)

---

## Quick Start (using Makefile)

```bash
# Build images, start bootstrap + 20 nodes, check peers, send messages
make all

# Or step by step:
make build       # Build both Docker images
make nodes       # Start bootstrap + all nodes
make test-peers  # Query bootstrap for registered peers
make test-messages  # Send random messages between nodes
make clean       # Stop and remove all containers
```

---

## Manual Commands

### Build images
```bash
docker network create p2p-net
docker build -t p2p-node .
docker build -t bootstrap-node -f bootstrap.Dockerfile .
```

### Start bootstrap
```bash
docker run -d --name bootstrap --network p2p-net -p 5000:5000 bootstrap-node
```

### Start nodes (example: 20 nodes)
```bash
for i in {1..20}; do
  PORT=$((5000 + i))
  docker run -d --name node$i --network p2p-net \
    -p $PORT:5000 \
    -e NODE_PORT=$PORT \
    -e NODE_URL="http://node$i:5000" \
    -e BOOTSTRAP_URL="http://bootstrap:5000" \
    p2p-node
done
```

### Check registered peers
```bash
curl http://localhost:5000/peers
```

### Send a message between two nodes
```bash
curl -X POST http://localhost:5002/message \
  -H "Content-Type: application/json" \
  -d '{"sender": "node1", "msg": "Hello node2!"}'
```

### Send messages across many nodes (15 random pairs)
```bash
for i in {1..15}; do
  src_port=$((5000 + (RANDOM % 20) + 1))
  target_port=$((5000 + (RANDOM % 20) + 1))
  echo "Sending from node$((src_port-5000)) to node$((target_port-5000))"
  curl -s -X POST "http://localhost:$target_port/message" \
    -H "Content-Type: application/json" \
    -d "{\"sender\": \"node$((src_port-5000))\", \"msg\": \"Hello node$((target_port-5000))!\"}"
done
```

---

## How It Works

1. **Bootstrap node** starts first and acts as a central registry.
2. Each **P2P node** registers its URL with bootstrap on startup, then fetches the current peer list.
3. Nodes communicate **directly** with each other via `/message` — no bootstrap needed after initial discovery.
4. A background thread on each node **periodically refreshes** its peer list by querying known peers, keeping the network self-healing.
