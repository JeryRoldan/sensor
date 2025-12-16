from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# ===== THINGSPEAK =====
CHANNEL_ID = "3189980"
READ_API_KEY = "HUH6AY63EEZMQW1E"
FIELD = 1

THINGSPEAK_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD}/last.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/distancia")
def obtener_distancia():
    try:
        response = requests.get(
            THINGSPEAK_URL,
            params={"api_key": READ_API_KEY},
            timeout=5
        )
        data = response.json()
        distancia = float(data[f"field{FIELD}"])
        return jsonify({"distancia": distancia})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
