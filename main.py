from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    code = data.get("code", "")
    question = data.get("message", "")

    prompt = f"""You are a helpful assistant named Elara that explains code and solves programming doubts.

    Here is the code:
    {code}

    User's question:
    {question}

    Respond clearly and concisely. Don't respond with anything other than code or programming related questions. If the question is not related to code or programming, just respond with "I can only help with code or programming related questions. and Don't think about the code or answer about it."""

    response = requests.post(OLLAMA_ENDPOINT, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    reply = response.json().get("response", "")
    return jsonify({"reply": reply})




# In‐memory store of events; replace with a proper DB for production
events = []

def record_event(event_type, payload):
    """Add timestamp + type and store the event."""
    event = {
        "type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": payload
    }
    events.append(event)
    # (Optional) broadcast via SocketIO here
    return event

@app.route("/api/vpn-disconnect", methods=["POST"])
def vpn_disconnect():
    """
    Called by your vpn-monitor script when a peer is offline.
    Expects JSON: { pubkey: str, last_handshake: int, timestamp: int }
    """
    payload = request.get_json(force=True)
    if not payload or "pubkey" not in payload:
        return jsonify({"error": "bad payload"}), 400

    event = record_event("vpn_disconnect", payload)
    app.logger.info(f"VPN disconnect: {payload['pubkey']}")
    return jsonify({"status": "ok", "event": event}), 200

@app.route("/api/dns-alert", methods=["POST"])
def dns_alert():
    """
    Called by a DNS monitor (if used) on blocked lookup.
    Expects JSON: { domain: str, client_ip: str, timestamp: str }
    """
    payload = request.get_json(force=True)
    if not payload or "domain" not in payload:
        return jsonify({"error": "bad payload"}), 400

    event = record_event("dns_alert", payload)
    app.logger.info(f"Blocked DNS lookup: {payload['domain']} from {payload['client_ip']}")
    return jsonify({"status": "ok", "event": event}), 200

@app.route("/api/events", methods=["GET"])
def get_events():
    """
    Returns all recorded events, ordered by timestamp.
    Your frontend can poll this endpoint to refresh its display.
    """
    return jsonify({"events": events}), 200

@app.route("/api/exam/start", methods=["POST"])
def exam_start():
    subprocess.Popen(["/path/to/start_exam.sh"])
    return {"status": "exam started"}, 200

@app.route("/api/exam/stop", methods=["POST"])
def exam_stop():
    subprocess.Popen(["/path/to/end_exam.sh"])
    return {"status": "exam stopped"}, 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)