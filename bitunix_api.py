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

def sign(payload: str, secret: str):
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

def place_market_order(symbol, side, risk_pct, tp_list, sl_pct):
    try:
        print("⚙️ Ejecutando orden en Bitunix...", flush=True)

        # Obtener saldo ficticio base (ejemplo 1000 USDT)
        balance = 1000  # ⚠️ Cambiar por consulta real si se necesita
        qty = round((balance * (risk_pct / 100)) / 1, 3)  # simplificado

        timestamp = get_timestamp()
        path = "/v1/private/order/create"
        url = BASE_URL + path

        body = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "MARKET",
            "quantity": qty,
            "timestamp": timestamp
        }

        payload = f"timestamp={timestamp}&symbol={symbol}&side={side.upper()}&type=MARKET&quantity={qty}"
        signature = sign(payload, API_SECRET)

        headers = {
            "X-BX-APIKEY": API_KEY,
            "X-BX-SIGNATURE": signature,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        result = response.json()

        print(f"✅ Orden enviada: {result}", flush=True)
        print(f"📌 TP (%): {tp_list} | SL (%): {sl_pct}", flush=True)

    except Exception as e:
        print("❌ Error al ejecutar orden:", e, flush=True)