import hmac
import hashlib
import time
import json
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "abc123")
API_SECRET = os.environ.get("API_SECRET", "xyz456")
BASE_URL = "https://fapi.bitunix.com"

def get_nonce():
    return os.urandom(16).hex()

def get_timestamp():
    return str(int(time.time() * 1000))

def generate_signature(nonce, timestamp, api_key, body, secret_key):
    message = nonce + timestamp + api_key + "" + body
    first_hash = hashlib.sha256(message.encode()).hexdigest()
    return hashlib.sha256((first_hash + secret_key).encode()).hexdigest()

@app.route("/", methods=["POST"])
def place_order():
    try:
        data = request.json
        symbol = data["symbol"]
        side = "BUY" if data["side"].lower() == "long" else "SELL"
        qty = str(data.get("qty", "0.3"))

        payload = {
            "symbol": symbol,
            "side": side,
            "orderType": "MARKET",
            "qty": qty,
            "tradeSide": "OPEN"
        }

        body = json.dumps(payload, separators=(",", ":"))
        nonce = get_nonce()
        timestamp = get_timestamp()
        sign = generate_signature(nonce, timestamp, API_KEY, body, API_SECRET)

        headers = {
            "api-key": API_KEY,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": sign,
            "Content-Type": "application/json"
        }

        url = BASE_URL + "/api/v1/futures/trade/place_order"
        res = requests.post(url, headers=headers, data=body)
        return jsonify(res.json()), res.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)