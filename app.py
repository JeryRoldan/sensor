from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# ===== THINGSPEAK =====
CHANNEL_ID = "3189980"
READ_API_KEY = "HUH6AY63EEZMQW1E"
FIELD = 1

app = Flask(__name__)

# ===== THINGSPEAK =====
CHANNEL_ID = "TU_CHANNEL_ID"
READ_API_KEY = "TU_READ_API_KEY"
FIELD = 1

FEEDS_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/historial")
def historial():
    try:
        response = requests.get(
            FEEDS_URL,
            params={
                "api_key": READ_API_KEY,
                "results": 20  # últimos 20 registros
            },
            timeout=5
        )
        data = response.json()

        filas = []
        for feed in data["feeds"]:
            if feed.get(f"field{FIELD}") is not None:
                filas.append({
                    "fecha": feed["created_at"],
                    "distancia": float(feed[f"field{FIELD}"])
                })

        return jsonify(filas)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)