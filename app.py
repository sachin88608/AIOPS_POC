from flask import Flask, request, jsonify
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace

# Initialize Flask app
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

# Load data and train model (do this once at startup)
data = load_breast_cancer()
X = data.data
y = data.target

# Split and scale (same as your code)
from sklearn.model_selection import train_test_split
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Build and train model
input_dim = X_train_scaled.shape[1]
model = keras.Sequential([
    keras.layers.Input(shape=(input_dim,)),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid")
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X_train_scaled, y_train, validation_data=(X_val_scaled, y_val), epochs=20, batch_size=32, verbose=0)

@app.route('/', methods=['GET'])
def home():
    return "API is running. Use POST /predict with JSON body."
    
# API endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from request
    data = request.get_json(force=True)
    X_new = np.array(data['features'])
    X_new_scaled = scaler.transform(X_new)
    y_proba = model.predict(X_new_scaled, verbose = 0)
    y_pred = (y_proba >= 0.5).astype(int).reshape(-1)
    return jsonify({'probabilities': y_proba.tolist(), 'predictions': y_pred.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
