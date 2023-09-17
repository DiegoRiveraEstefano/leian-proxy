import os
from ApiKey.ApiKeyManager import ApiKeyManager
from flask import Flask
from flask import request
from dotenv import load_dotenv
import json
import requests

load_dotenv()
app = Flask(__name__)

proxy_key = os.getenv("PROXY_KEY")
api_key_manager = ApiKeyManager()


@app.post("/v1/complete")
def get_completion():
    token = request.headers.get("x-api-key")
    if token != proxy_key:
        return 404
    print("Get Completion")
    rs = api_key_manager.get_completion("SourceGraph", request.json)
    if type(rs) == int:
        print(rs)
        return app.response_class(
            response={"No existen api keys o las que estan se agotaron"},
            status=rs,
            mimetype='application/json'
        )
    print("Sending Completion")
    response = app.response_class(
        response=json.dumps(
            {
                "completion": rs,
                "stop_reason": "stop_sequence"
            }
        ),
        status=200,
        mimetype='application/json'
    )
    return response


@app.post('/v1/limit')
def get_limit():
    return requests.post(
        url="https://sourcegraph.com/.api/completions/limit"
    )