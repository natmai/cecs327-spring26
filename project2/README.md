# A Bite of Distributed Communication

## Files

### Task 1 (Anycast TCP)

* `server.py` – TCP server
* `client.py` – TCP client
* `Dockerfile` – builds server/client image
* `docker-compose.yml` – runs 3 servers and 1 client

### Task 2 (Multicast UDP)

* `multicast_sender.py` – sends JSON and binary data
* `multicast_receiver.py` – receives multicast messages
* `Dockerfile` – builds multicast image
* `docker-compose.yml` – runs senders and receivers

---

## Build

From each task directory (`task1/` or `task2/`) run:

```sh
docker compose build
```

---

## Task 1 – Anycast (TCP)

### Run

```sh
docker compose up
```

Run client multiple times:

```sh
docker compose run --rm client
```

### Example Output

```sh
Received: Hello from server1
Received: Hello from server2
Received: Hello from server3
```

---

## Task 2 – Multicast (UDP)

### Run

```sh
docker compose up
```

### Example Output

Receiver:

```sh
Joined multicast group 224.1.1.1:5007
Received JSON from ('172.x.x.x', 5007): {'sensor': 'temp', 'value': 20.5}
Received JSON from ('172.x.x.x', 5007): {'sensor': 'humidity', 'value': 30.0}
Leaving multicast group
```

---

## Monitor Traffic

Run inside a container:

```sh
docker exec -it <container_id> tcpdump -i eth0 udp port 5007
```

---

