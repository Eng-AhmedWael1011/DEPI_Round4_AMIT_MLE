def train(model , x_train , y_train , batch_size , validation_split , epochs):
    
    print('Training model...')
    history = model.fit(x_train , y_train , batch_size= batch_size, validation_split= validation_split , epochs=epochs)
    
    print('model_trained')

    return history
