from flask import Flask
from flask import request
from pprint import pprint
import json

app = Flask(__name__)

with open("secrets.json", "r") as f:
    secrets = json.load(f)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test', methods=['POST'])
def test_route():
    payload = request.get_json()
    
    print("Request Body:")
    pprint(payload)
    print()
    print("Secrets:")
    pprint(secrets)

    return {
        "request_body" : payload,
        "secrets" : secrets
    }

