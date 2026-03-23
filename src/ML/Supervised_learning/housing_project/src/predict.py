import joblib
import numpy as np

def predict(input_data, model_path):
    model = joblib.load(model_path)
    return model.predict(np.array(input_data).reshape(1,-1))