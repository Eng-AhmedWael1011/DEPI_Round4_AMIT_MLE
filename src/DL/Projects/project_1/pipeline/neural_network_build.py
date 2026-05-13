from tensorflow.keras import layers , Sequential

def build_nn(input_size , num_classes , activation , optimizer , loss , metric):

    print("Building Neural network...")
    model = Sequential([
        layers.Input(shape=(input_size,)), # assuring the samples flattend 
        layers.Dense(1000 , activation=activation), #h1
        layers.Dense(500 , activation=activation ), #h2
        layers.Dense(num_classes , activation='softmax' ), # Output layer
    ])
    
    model.summary()
    print("Success")

    print('compiling model...')

    model.compile(optimizer=optimizer , loss= loss , metrics=[metric])

    return model

