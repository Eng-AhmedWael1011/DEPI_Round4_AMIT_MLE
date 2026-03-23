from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.pipeline import Pipeline


def train_linear_model(x_train, y_train):
    model = Pipeline([
        ('scaler', MinMaxScaler()),
        ('linear', LinearRegression())
    ])
    model.fit(x_train , y_train)
    return model

def train_polyomial(x_train , y_train , degree = 2):
    model = Pipeline([
        ('poly', PolynomialFeatures(degree=degree)),
        ('linear', LinearRegression())
    ])

    model.fit(x_train , y_train)
    return model

