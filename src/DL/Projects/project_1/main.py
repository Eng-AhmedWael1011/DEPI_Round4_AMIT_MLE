from pipeline.data_loader import load_data
from pipeline.train import train
from pipeline.evaluate import evaluate
from pipeline.neural_network_build import build_nn
from config import *

def run():
    x_train, y_train, x_test, y_test = load_data(INPUT_SIZE , NUM_CLASSES)

    model = build_nn(INPUT_SIZE, NUM_CLASSES, 'relu', 'adam',
                     'categorical_crossentropy', 'accuracy')

    train(model, x_train, y_train, BATCH_SIZE, VALIDATION_SPLIT, EPOCHS)

    evaluate(model, x_test, y_test)

if __name__ == "__main__":
    run()