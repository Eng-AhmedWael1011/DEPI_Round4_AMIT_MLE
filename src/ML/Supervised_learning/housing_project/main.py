import os
import json
from flask import Flask, request, jsonify, render_template

from src.data_loader import data_loader
from src.preprocess import split_data
from src.train import train_linear_model, train_polyomial
from src.evaluate import evaluate_model
from src.save_model import save_model
from src.predict import predict as run_prediction

app = Flask(__name__)

# Route for the beautiful homepage
@app.route("/")
def home():
    # Render a premium frontend template
    return render_template("index.html")

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Expecting JSON input
        data = request.json.get("features", {})
        
        # Features are RM, LSTAT, PTRATIO
        rm = float(data.get("RM", 6.0))
        lstat = float(data.get("LSTAT", 12.0))
        ptratio = float(data.get("PTRATIO", 18.0))
        
        # Structure it as a 1D array/list exactly.
        features = [rm, lstat, ptratio]
        
        # Attempt to use the Linear model or Polynomial model
        # Try finding Polynomial first as it's usually better, else Linear
        model_path = "models/Polynomial.pkl"
        if not os.path.exists(model_path):
            model_path = "models/Linear.pkl"
            
        if not os.path.exists(model_path):
            return jsonify({
                "status": "error",
                "message": "No models trained yet. Please train the models first.",
                "prediction": "N/A"
            })
            
        pred = run_prediction(features, model_path)[0]
        
        return jsonify({
            "status": "success",
            "received_features": features,
            "prediction": f"${pred:,.2f}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Training route
@app.route("/train", methods=["POST"])
def train():
    try:
        # Load the data
        data_path = r"C:\Users\Ahmed\Desktop\DEPI\DEPI Round 4\MLE SESSION TASKS\DEPI_Round4_AMIT_MLE\src\ML\Supervised_learning\housing_project\data\housing.csv"
        data = data_loader(data_path)

        # split the data
        X_train, X_test, Y_train, Y_test = split_data(data, "MEDV")

        # Train the models
        linear_model = train_linear_model(X_train, Y_train)
        poly_model = train_polyomial(X_train, Y_train)

        # model Evaluation Scores - Test Data
        l_res_test = evaluate_model(linear_model, X_test, Y_test)
        p_res_test = evaluate_model(poly_model, X_test, Y_test)
        
        # model Evaluation Scores - Train Data
        l_res_train = evaluate_model(linear_model, X_train, Y_train)
        p_res_train = evaluate_model(poly_model, X_train, Y_train)

        # convert to floats to avoid JSON serializable issues
        linear_test = {k: float(v) for k, v in l_res_test.items()}
        poly_test = {k: float(v) for k, v in p_res_test.items()}
        linear_train = {k: float(v) for k, v in l_res_train.items()}
        poly_train = {k: float(v) for k, v in p_res_train.items()}

        # Choose the best model based on R2 test score by default
        if poly_test["r2"] > linear_test["r2"]:
            best_model = poly_test
            best_name = "Polynomial"
            best_obj = poly_model
        else:
            best_model = linear_test
            best_name = "Linear"
            best_obj = linear_model
            
        # Ensure models directory exists and save best
        os.makedirs("models", exist_ok=True)
        save_model(best_obj, f"models/{best_name}.pkl")
        
        # Save both if needed later, but standard is saving best
        save_model(linear_model, f"models/Linear.pkl")
        save_model(poly_model, f"models/Polynomial.pkl")
        
        # Generate data for the scatter plot (take up to 100 test samples)
        import numpy as np
        num_samples = min(100, len(Y_test))
        actuals = Y_test.values[:num_samples].tolist() if hasattr(Y_test, 'values') else Y_test[:num_samples]
        
        lin_preds = linear_model.predict(X_test[:num_samples])
        poly_preds = poly_model.predict(X_test[:num_samples])
        
        lin_preds_list = lin_preds.tolist() if hasattr(lin_preds, 'tolist') else lin_preds
        poly_preds_list = poly_preds.tolist() if hasattr(poly_preds, 'tolist') else poly_preds

        scatter_data = {
            "actual": actuals,
            "linear_pred": lin_preds_list,
            "poly_pred": poly_preds_list
        }

        return jsonify({
            "status": "success",
            "message": f"Successfully trained pipelines. Default Best Model (R² Test): {best_name}",
            "best_model": best_name,
            "linear_metrics": { "train": linear_train, "test": linear_test },
            "poly_metrics": { "train": poly_train, "test": poly_test },
            "scatter_data": scatter_data
        })
    except Exception as e:
        import traceback
        return jsonify({
            "status": "error", "message": str(e), "traceback": traceback.format_exc(), 
            "linear_metrics": {}, "poly_metrics": {}, "scatter_data": {}
        })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
