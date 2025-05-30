import hmac
import hashlib
import time
import requests
import os

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BASE_URL = "https://api.bitunix.com"

def get_timestamp():
    return str(int(time.time() * 1000))

def sign(payload: dict, secret: str):
    sorted_items = sorted(payload.items())
    query_string = '&'.join([f"{k}={v}" for k, v in sorted_items])
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def place_market_order(symbol, side, risk_pct, tp_list, sl_pct):
    try:
        print("⚙️ Ejecutando orden en Bitunix...", flush=True)

        balance = 1000  # Simulado. Ideal: obtener con endpoint balance
        qty = round((balance * (risk_pct / 100)) / 1, 3)  # simplificado

        timestamp = get_timestamp()
        path = "/open-api/api/v1/order"
        url = BASE_URL + path

        data = {
            "symbol": symbol,
            "side": "BUY" if side.lower() == "long" else "SELL",
            "type": "MARKET",
            "quantity": qty,
            "timestamp": timestamp
        }

        signature = sign(data, API_SECRET)
        data["signature"] = signature

        headers = {
            "X-BX-APIKEY": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        print(f"✅ Orden enviada: {result}", flush=True)
        print(f"📌 TP (%): {tp_list} | SL (%): {sl_pct}", flush=True)

    except Exception as e:
        print("❌ Error al ejecutar orden:", e, flush=True)