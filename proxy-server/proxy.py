from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mapping of languages to their respective container endpoints
LANGUAGE_TO_CONTAINER = {
    "python": "http://python-container:5000/execute",  # Python container endpoint
    "c": "http://c-container:5000/execute",           # C container endpoint
}

@app.route('/execute', methods=['POST'])
def main_server():
    try:
        # Get the request payload
        data = request.get_json()
        code = data.get("code")
        language = data.get("language")

        # Validate the input
        if not code or not language:
            return jsonify({"error": "Both 'code' and 'language' fields are required."}), 400

        container_url = LANGUAGE_TO_CONTAINER.get(language.lower())
        if not container_url:
            return jsonify({"error": f"Unsupported language: {language}"}), 400

        response = requests.post(container_url, json={"code": code})

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to the container.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # Main server runs on port 8000
