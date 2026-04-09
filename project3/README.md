# A Bite of Peer-to-Peer

## Files

* `node.py` – P2P node application (client + server)
* `bootstrap.py` – Bootstrap registry node
* `Dockerfile` – builds the P2P node image
* `bootstrap.Dockerfile` – builds the bootstrap node image
* `requirements.txt` – Python dependencies
* `Makefile` – automates build, run, and test

---

## Build

```sh
docker network create p2p-net
docker build -t p2p-node .
docker build -t bootstrap-node -f bootstrap.Dockerfile .
```

---

## Run

### Start bootstrap node

```sh
docker run -d --name bootstrap --network p2p-net -p 5050:5000 bootstrap-node
```

### Start 50 P2P nodes

```sh
for i in {1..50}; do
  PORT=$((5000 + i))
  docker run -d --name node$i --network p2p-net \
    -p $PORT:5000 \
    -e NODE_PORT=$PORT \
    -e NODE_URL="http://node$i:5000" \
    -e BOOTSTRAP_URL="http://bootstrap:5000" \
    p2p-node
done
```

### Or use the Makefile

```sh
make all
```

---

## Test

### Check bootstrap is running

```sh
curl http://localhost:5050/
```

### Check registered peers

```sh
curl http://localhost:5050/peers | python3 -m json.tool
```

### Send a message between two nodes

```sh
curl -s -X POST http://localhost:5002/message \
  -H "Content-Type: application/json" \
  -d '{"sender": "node1", "msg": "Hello node2!"}'
```

### Send messages across many nodes

```sh
for i in {1..15}; do
  src=$((RANDOM % 50 + 1))
  dst=$((RANDOM % 50 + 1))
  echo "Sending from node$src to node$dst"
  curl -s -X POST http://localhost:$((5000+dst))/message \
    -H "Content-Type: application/json" \
    -d '{"sender": "node'"$src"'", "msg": "Hello node'"$dst"' from node'"$src"'"}'
  echo ""
done
```

### Example Output

```sh
Sending from node12 to node37
{"status": "received"}

Sending from node4 to node19
{"status": "received"}
```

---

## View Logs

```sh
docker logs bootstrap --tail 30
docker logs node1 --tail 30
```

### Example Output

```sh
[Bootstrap] Registered peer: http://node1:5000 | Total: 1
[Bootstrap] Registered peer: http://node2:5000 | Total: 2
[abcd1234] Registered with bootstrap at http://bootstrap:5000
[abcd1234] Received message from node12: Hello node37 from node12
```

---

## Monitor Containers

```sh
docker ps | grep -E "bootstrap|node" | wc -l
```

---

## Clean Up

```sh
make clean
```

Or manually:

```sh
docker rm -f $(docker ps -aq)
docker network rm p2p-net
```

---
