"""
Flask backend for MNIST Digit Recognition Web Application.
Loads a trained Keras model and exposes a /predict endpoint.
"""

import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------------
# Load model ONCE at startup
# ---------------------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.keras")

# Fallback to .h5 if .keras file doesn't exist
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.h5")

print(f"Loading model from: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print("[OK] Model loaded successfully.")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the frontend page."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict a handwritten digit.

    Expects JSON: { "image": [<784 float values>] }
    Returns JSON:  { "prediction": int, "confidence": float }
    """
    try:
        # --- Validate request ---
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error": "Invalid JSON payload."}), 400

        if "image" not in data:
            return jsonify({"error": "Missing key 'image' in JSON payload."}), 400

        image_data = data["image"]

        if not isinstance(image_data, list):
            return jsonify({"error": "'image' must be a list of 784 float values."}), 400

        if len(image_data) != 784:
            return jsonify({
                "error": f"'image' must contain exactly 784 values, got {len(image_data)}."
            }), 400

        # --- Preprocess ---
        x = np.array(image_data, dtype=np.float32)  # Convert to numpy
        x = x.reshape(1, 784)                        # Reshape to (1, 784)

        # --- Predict ---
        preds = model.predict(x, verbose=0)
        predicted_class = int(np.argmax(preds))
        confidence = float(np.max(preds))

        return jsonify({
            "prediction": predicted_class,
            "confidence": confidence,
            "probabilities": [float(p) for p in preds[0]]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
