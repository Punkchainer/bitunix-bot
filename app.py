from flask import Flask, request, jsonify
from bitunix_api import place_market_order

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.json
        required_keys = ["symbol", "side", "risk_pct", "tp_pct", "sl_pct"]
        if not all(key in data for key in required_keys):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        print("📩 Alerta recibida desde TradingView:", flush=True)
        print(f"  ▸ Symbol: {data['symbol']}", flush=True)
        print(f"  ▸ Side: {data['side']}", flush=True)
        print(f"  ▸ Risk: {data['risk_pct']}%", flush=True)
        print(f"  ▸ Take Profits: {data['tp_pct']}", flush=True)
        print(f"  ▸ Stop Loss: {data['sl_pct']}%", flush=True)

        # Ejecutar orden en Bitunix
        place_market_order(
            symbol=data['symbol'],
            side=data['side'],
            risk_pct=data['risk_pct'],
            tp_list=data['tp_pct'],
            sl_pct=data['sl_pct']
        )

        return jsonify({"status": "success", "message": "Orden ejecutada"}), 200

    except Exception as e:
        print("❌ Error al procesar la alerta:", e, flush=True)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)