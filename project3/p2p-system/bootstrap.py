from flask import Flask, request, jsonify

app = Flask(__name__)

# Registry of all nodes that have checked in
registered_peers = set()


@app.route("/", methods=["GET"])
def index():
    """Health check for the bootstrap node."""
    return jsonify({"message": "Bootstrap node is running!"})


@app.route("/register", methods=["POST"])
def register():
    """
    Nodes POST their URL here on startup.
    Bootstrap stores it and returns the full current peer list
    so the new node can immediately discover everyone else.
    """
    data = request.get_json()
    peer_url = data.get("url")
    if peer_url:
        registered_peers.add(peer_url)
        print(f"[Bootstrap] Registered peer: {peer_url} | Total: {len(registered_peers)}")
    return jsonify({"status": "registered", "peers": list(registered_peers)})


@app.route("/peers", methods=["GET"])
def get_peers():
    """Return the complete list of registered peers."""
    return jsonify({"peers": list(registered_peers)})


if __name__ == "__main__":
    print("[Bootstrap] Bootstrap node starting on port 5000...")
    app.run(host="0.0.0.0", port=5000)
