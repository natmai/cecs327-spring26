from flask import Flask, request, jsonify
import uuid
import os
import requests
import threading
import time

app = Flask(__name__)

# Unique identifier for this node
node_id = str(uuid.uuid4())

# Read environment variables set by Docker at runtime
NODE_URL = os.environ.get("NODE_URL", "http://localhost:5000")
BOOTSTRAP_URL = os.environ.get("BOOTSTRAP_URL", "http://bootstrap:5000")

# Set of known peers (excluding self)
peers = set()


# ---------------------------------------------------------------------------
# Bootstrap registration
# ---------------------------------------------------------------------------

def register_with_bootstrap():
    """Register this node with the bootstrap node and fetch the initial peer list."""
    try:
        # Tell bootstrap we exist
        requests.post(
            f"{BOOTSTRAP_URL}/register",
            json={"url": NODE_URL},
            timeout=5
        )
        print(f"[{node_id[:8]}] Registered with bootstrap at {BOOTSTRAP_URL}")

        # Grab whatever peers bootstrap already knows about
        response = requests.get(f"{BOOTSTRAP_URL}/peers", timeout=5)
        data = response.json()
        for peer in data.get("peers", []):
            if peer != NODE_URL:
                peers.add(peer)
        print(f"[{node_id[:8]}] Initial peer list: {peers}")

    except Exception as e:
        print(f"[{node_id[:8]}] Could not reach bootstrap: {e}")


# ---------------------------------------------------------------------------
# Peer discovery (runs in background thread)
# ---------------------------------------------------------------------------

def discover_peers():
    """
    Periodically ask known peers for their peer lists so the network
    stays connected even after the bootstrap node goes away.
    """
    while True:
        time.sleep(15)
        new_peers = set()
        for peer in list(peers):
            try:
                response = requests.get(f"{peer}/peers", timeout=3)
                for p in response.json().get("peers", []):
                    if p != NODE_URL:
                        new_peers.add(p)
            except Exception:
                pass  # Peer may be temporarily unreachable
        peers.update(new_peers)


# ---------------------------------------------------------------------------
# Flask routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """Health check — confirms the node is alive."""
    return jsonify({"message": f"Node {node_id} is running!"})


@app.route("/register", methods=["POST"])
def register():
    """Allow another peer to register itself with this node."""
    data = request.get_json()
    peer_url = data.get("url")
    if peer_url and peer_url != NODE_URL:
        peers.add(peer_url)
        print(f"[{node_id[:8]}] Registered new peer: {peer_url}")
    return jsonify({"status": "registered", "peers": list(peers)})


@app.route("/peers", methods=["GET"])
def get_peers():
    """Return the list of peers this node currently knows about."""
    return jsonify({"peers": list(peers)})


@app.route("/message", methods=["POST"])
def receive_message():
    """Receive a message from another node."""
    data = request.get_json()
    sender = data.get("sender", "unknown")
    msg = data.get("msg", "")
    print(f"[{node_id[:8]}] Received message from {sender}: {msg}")
    return jsonify({"status": "received"})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Wait briefly for bootstrap to be ready before registering
    time.sleep(2)
    register_with_bootstrap()

    # Start background peer-discovery thread
    threading.Thread(target=discover_peers, daemon=True).start()

    app.run(host="0.0.0.0", port=5000)
