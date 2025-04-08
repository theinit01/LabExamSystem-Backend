from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    code = data.get("code", "")
    question = data.get("message", "")

    prompt = f"""YYou are a helpful assistant that explains code and solves programming doubts.

Here is the code:
{code}

User's question:
{question}

Respond clearly and concisely. Don't respond with anything other than code or study related questions. If the question is not related to code or study, respond with "I can only help with code or study related questions."""

    response = requests.post(OLLAMA_ENDPOINT, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    reply = response.json().get("response", "")
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)