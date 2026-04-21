import os, hashlib
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

NODE_NAME = os.environ.get("NODE_NAME", "node1")
PEERS_ENV = os.environ.get("PEERS", "")
ALL_NODES = ([f"http://{NODE_NAME}:5000"] + PEERS_ENV.split(",")) if PEERS_ENV else [f"http://{NODE_NAME}:5000"]
ALL_NODES = sorted(set(ALL_NODES))
SELF_URL = f"http://{NODE_NAME}:5000"

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f"./storage/{file.filename}")
    return jsonify({"status": "uploaded", "filename": file.filename})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path = f"./storage/{filename}"
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    return send_from_directory('./storage', filename)

kv_store = {}

@app.route('/kv', methods=['POST'])
def kv_post():
    data = request.get_json()
    key = data['key']
    value = data['value']

    responsible = hash_key_to_node(key)
    if responsible != SELF_URL:
        res = requests.post(f"{responsible}/kv", json=data)
        return jsonify(res.json())

    kv_store[key] = value
    return jsonify({"key": key, "status": "success", "value": value})

@app.route('/kv/<key>', methods=['GET'])
def kv_get(key):
    responsible = hash_key_to_node(key)
    if responsible != SELF_URL:
        res = requests.get(f"{responsible}/kv/{key}")
        return jsonify(res.json())

    if key not in kv_store:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"key": key, "value": kv_store[key]})

def hash_key_to_node(key):
    h = int(hashlib.sha1(key.encode()).hexdigest(), 16)
    return ALL_NODES[h % len(ALL_NODES)]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "node": NODE_NAME})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)