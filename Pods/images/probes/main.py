from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    response = {}
    response["USER"] = os.environ.get("USER", "ashry")
    response["TOKEN"] = os.environ.get("TOKEN", "1234567890")
    return jsonify(response=response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
