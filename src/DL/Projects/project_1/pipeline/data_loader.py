import tensorflow as tf
from tensorflow.keras.datasets import mnist

def load_data(input_size , num_classes):

    print("LOADING DATA...")

    (X_train , y_train) , (x_test , y_test) = mnist.load_data()

    print("DATA LOADED SUCCESSFULLY, NOW PREPROCESSING...")
    # Normalizing the images
    x_train_norm = X_train.astype('float32') / 255.0
    x_test_norm = x_test.astype('float32') / 255.0

    # reshaping the data
    x_train = x_train_norm.reshape(-1 , input_size)
    x_test = x_test_norm.reshape(-1 , input_size)

    # one hot encoding for Target Y
    y_train_oh = tf.keras.utils.to_categorical(y_train ,num_classes)
    y_test_oh = tf.keras.utils.to_categorical(y_test , num_classes)

    print("SUCCESS.")
    return x_train , y_train_oh , x_test , y_test_oh