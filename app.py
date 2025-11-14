# Simple starter app for Casa-inteligente
# This is a placeholder Flask app that demonstrates where the model would be loaded
# and how gestures could be exposed via a small HTTP API. Replace with your real
# inference code and the trained model (tm_model/gestos.h5).

from flask import Flask, jsonify, request
import os

app = Flask(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'tm_model', 'gestos.h5')
LABELS_PATH = os.path.join(os.path.dirname(__file__), 'tm_model', 'labels.txt')

@app.route('/')
def index():
    return jsonify({'message': 'Casa-inteligente placeholder app', 'model_exists': os.path.exists(MODEL_PATH)})

@app.route('/predict', methods=['POST'])
def predict():
    # Placeholder prediction endpoint. Expects an image (multipart/form-data) or
    # base64 payload in JSON. Currently returns a fixed response.
    data = request.json or {}
    return jsonify({'gesture': 'placeholder', 'confidence': 0.0, 'received': bool(data)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)