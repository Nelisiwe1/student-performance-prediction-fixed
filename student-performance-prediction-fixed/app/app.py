from flask import Flask, request, jsonify, send_file
import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "StudentsPerformance.csv")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

# Create plots folder if it doesn't exist
os.makedirs(PLOTS_DIR, exist_ok=True)

# Load model
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Run training script first to create model.pkl")
    return joblib.load(MODEL_PATH)

# Health check
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "Flask app is running!"})

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    df = pd.DataFrame([data])
    model = load_model()
    pred = float(np.round(model.predict(df)[0], 2))
    return jsonify({"predicted_avg_score": pred})

# Generate and serve visualizations
@app.route('/plots/<plot_name>', methods=['GET'])
def get_plot(plot_name):
    # Load data
    df = pd.read_csv(DATA_PATH, sep=';')  # adjust sep if using student-mat dataset
    sns.set(style='whitegrid')

    plot_file = os.path.join(PLOTS_DIR, plot_name)

    if plot_name == "score_distribution.png":
        plt.figure(figsize=(10,5))
        sns.histplot(df['G3'], kde=True, color='blue', label='Final Grade (G3)')
        plt.title('Distribution of Final Grades')
        plt.savefig(plot_file)
        plt.close()
    elif plot_name == "G3_by_sex.png":
        plt.figure(figsize=(8,5))
        sns.boxplot(x='sex', y='G3', data=df)
        plt.title('Final Grade by Sex')
        plt.savefig(plot_file)
        plt.close()
    elif plot_name == "correlation_heatmap.png":
        numeric_cols = df.select_dtypes(include='number')
        plt.figure(figsize=(10,8))
        sns.heatmap(numeric_cols.corr(), annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.savefig(plot_file)
        plt.close()
    else:
        return jsonify({"error": "Plot not found"}), 404

    return send_file(plot_file, mimetype='image/png')

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to Student Performance API!",
        "routes": ["/ping", "/predict", "/plots/score_distribution.png", "/plots/G3_by_sex.png", "/plots/correlation_heatmap.png"]
    })

if __name__ == '__main__':
    app.run(debug=True)
