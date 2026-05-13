def evaluate(model , x_test , y_test):
    test_loss , test_accuracy = model.evaluate(x_test , y_test)
    print('TEST LOSS: ', test_loss)
    print('TEST ACCURACY: ', test_accuracy)
    return test_loss , test_accuracy
