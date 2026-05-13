"""
Train the MNIST model and save it as model.keras for the web application.
Uses the existing pipeline modules.
"""

import os
import sys

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline.data_loader import load_data
from pipeline.train import train
from pipeline.evaluate import evaluate
from pipeline.neural_network_build import build_nn
from config import *


def train_and_save():
    """Train the MNIST neural network and save the model."""

    # 1. Load & preprocess data
    x_train, y_train, x_test, y_test = load_data(INPUT_SIZE, NUM_CLASSES)

    # 2. Build the neural network
    model = build_nn(
        INPUT_SIZE, NUM_CLASSES,
        'relu', 'adam',
        'categorical_crossentropy', 'accuracy'
    )

    # 3. Train
    train(model, x_train, y_train, BATCH_SIZE, VALIDATION_SPLIT, EPOCHS)

    # 4. Evaluate
    evaluate(model, x_test, y_test)

    # 5. Save the trained model
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.keras")
    model.save(save_path)
    print(f"\n[OK] Model saved to: {save_path}")


if __name__ == "__main__":
    train_and_save()
