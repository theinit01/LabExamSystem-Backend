from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/execute', methods=['POST'])
def execute_c_code():
    source_file = None
    binary_file = None

    try:
        # Get code from the request
        code = request.json.get('code')
        if not code:
            return jsonify({'error': 'No code provided'}), 400

        # Generate unique filenames using UUID
        unique_id = str(uuid.uuid4())
        source_file = f"{unique_id}.c"
        binary_file = f"{unique_id}.out"

        # Write the code to a file
        with open(source_file, "w") as f:
            f.write(code)

        # Compile the code
        compile_process = subprocess.run(
            ["gcc", source_file, "-o", binary_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )

        if compile_process.returncode != 0:
            return jsonify({'error': compile_process.stderr}), 400

        # Execute the compiled binary
        execute_process = subprocess.run(
            [f"./{binary_file}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )

        if execute_process.returncode == 0:
            return jsonify({'output': execute_process.stdout})
        else:
            return jsonify({'error': execute_process.stderr})

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if source_file and os.path.exists(source_file):
            os.remove(source_file)
        if binary_file and os.path.exists(binary_file):
            os.remove(binary_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
