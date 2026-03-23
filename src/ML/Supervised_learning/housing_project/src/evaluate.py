from sklearn.metrics import r2_score , mean_squared_error , root_mean_squared_error, mean_absolute_error


def evaluate_model(model, x_test , y_test):
    """Model Evaluation"""
    y_pred = model.predict(x_test)

    r2 = r2_score(y_test , y_pred)
    mse = mean_squared_error(y_test , y_pred)

    return {
        "r2" : r2,
        "mse" : mse,
        "mae" : mean_absolute_error(y_test, y_pred),
        "rmse" : root_mean_squared_error(y_test, y_pred)
    }