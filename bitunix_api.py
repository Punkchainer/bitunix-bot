import hmac
import hashlib
import time
import json
import os
import requests

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BASE_URL = "https://fapi.bitunix.com"

def get_nonce():
    return os.urandom(16).hex()

def get_timestamp():
    return str(int(time.time() * 1000))

def generate_signature(nonce, timestamp, api_key, body, secret_key):
    message = nonce + timestamp + api_key + "" + body
    first_hash = hashlib.sha256(message.encode()).hexdigest()
    signature = hashlib.sha256((first_hash + secret_key).encode()).hexdigest()
    return signature

def place_market_order(symbol, side, risk_pct, tp_list, sl_pct):
    try:
        print("⚙️ Ejecutando orden copytrading (MASTER)...", flush=True)

        balance = 1000  # Simulado
        qty = round((balance * (risk_pct / 100)) / 1, 3)

        url = BASE_URL + "/api/v1/copytrade/master/order"

        payload = {
            "symbol": symbol,
            "side": "BUY" if side.lower() == "long" else "SELL",
            "orderType": "MARKET",
            "leverage": 10,
            "positionType": "ISOLATED",
            "tradeType": "OPEN",
            "qty": str(qty)
        }

        body = json.dumps(payload, separators=(",", ":"))
        nonce = get_nonce()
        timestamp = get_timestamp()
        signature = generate_signature(nonce, timestamp, API_KEY, body, API_SECRET)

        headers = {
            "api-key": API_KEY,
            "nonce": nonce,
            "timestamp": timestamp,
            "sign": signature,
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        result = response.json()

        print(f"✅ Orden copytrade enviada: {result}", flush=True)
        print(f"📌 TP (%): {tp_list} | SL (%): {sl_pct}", flush=True)

    except Exception as e:
        print("❌ Error al ejecutar orden:", e, flush=True)