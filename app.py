"""
ALGORITHM 6 — BACKEND PREDICTION API (RESULT DELIVERY)
------------------------------------------------------------
START
1. Receive prediction request (crop, months-ahead) from frontend
2. Trigger Algorithms 1-5 in sequence
3. Collect the final predicted price list
4. Package results into structured JSON
5. Send response back to the frontend
END
"""

import os
import glob
from flask import Flask, render_template, request, jsonify

from utils.predictor import predict_future_prices

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def available_crops():
    return sorted(
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(DATA_DIR, "*.csv"))
    )


@app.route("/")
def index():
    return render_template("index.html", crops=available_crops())


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True) or {}
    crop = str(payload.get("crop", "")).strip()
    months_ahead = payload.get("months_ahead")

    # --- basic validation (EH-01 / EH-02 style error handling) ---
    if not crop:
        return jsonify({"success": False, "message": "Please select a crop."}), 400
    try:
        months_ahead = int(months_ahead)
        if months_ahead <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Months ahead must be a positive number."}), 400

    try:
        results = predict_future_prices(crop, months_ahead)
    except FileNotFoundError:
        return jsonify({
            "success": False,
            "message": f"Model not trained for '{crop}'. Run: python train_model.py {crop}",
        }), 404
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    return jsonify({"success": True, "crop": crop, "predictions": results})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
