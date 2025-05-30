from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("🔔 Alerta recibida:", data, flush=True)
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        print("❌ Error al procesar alerta:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)