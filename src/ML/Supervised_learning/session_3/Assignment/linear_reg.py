import numpy as np
import matplotlib.pyplot as plt




class LinearRegressionGD_AhmedWael:
    """
    Linear Regression using Gradient Descent with optional L1 (Lasso) and L2 (Ridge) regularization.

    Attributes
    ----------
    learning_rate : float
        Step size for gradient descent updates.
    gd_iterations : int
        Number of iterations to run gradient descent.
    theta_0 : float
        Model slope (weight).
    theta_1 : float
        Model intercept (bias).
    MSE : list
        Placeholder list for mean squared error values (not currently used).
    SSE : list
        History of sum of squared errors across iterations.
    reg_type : str, optional
        Type of regularization ('ridge', 'lasso', or None).
    lam : float
        Regularization strength (λ).
    y_hat : ndarray
        Latest predictions from the model.

    Methods
    -------
    gradiant_descent(x, y, y_hat):
        Computes parameter gradients with optional Ridge or Lasso penalty.
    fit(x, y):
        Trains the model using gradient descent, updates parameters, and logs progress.
    predict(x):
        Generates predictions for input features.
    plot_training(x, y):
        Plots SSE over iterations and regression line against data points.
    """

    def __init__(self , lr , n_iters , reg_type = None , lam = 0.0):
        self.learning_rate = lr
        self.gd_iterations = n_iters
        self.theta_0 = 0
        self.theta_1 = 0
        self.MSE = []
        self.SSE = []
        self.reg_type = reg_type
        self.lam = lam
        self.y_hat = None

    def gradiant_descent(self, x , y , y_hat):
        delta_theta_0 = 2 * np.mean((y_hat - y) * x)
        delta_theta_1 = 2 * np.mean((y_hat - y))

        if self.reg_type == "ridge":
            delta_theta_0 += self.lam * self.theta_0
            delta_theta_1 += self.lam * self.theta_1
        elif self.reg_type == "lasso":
            delta_theta_0 += self.lam * np.sign(self.theta_0)
            delta_theta_1 += self.lam * np.sign(self.theta_1)
        return delta_theta_0 , delta_theta_1


    def fit(self , x , y):

        for i in range(self.gd_iterations):

            y_hat = self.theta_0 * x + self.theta_1

            sse = (np.sum((y_hat - y)**2))
            self.SSE.append(sse)

            delta_theta_0 , delta_theta_1 = self.gradiant_descent(x , y , y_hat)

            self.theta_0 -= self.learning_rate * delta_theta_0
            self.theta_1 -= self.learning_rate * delta_theta_1

            if i %20 == 0:
                print(f"No.of iters is {i}\nSSE is {sse}\nTheta_0 is {self.theta_0}\ntheta_1 is {self.theta_1}")
                print('-'*20)

    def predict(self , x):

        y_hat = self.theta_0 * x + self.theta_1
        self.y_hat = y_hat
        return y_hat
    

    def plot_training(self , x , y):
        
        plt.figure(figsize=(14,2))
        plt.subplot(1,2,1)
        plt.plot(self.SSE , label="SSE")
        plt.xlabel('num of iterations')
        plt.ylabel('SSE values')
        plt.title('SEE over iteration')
        plt.legend()

        # plt.subplot(1,2,2)
        # plt.scatter(x, y, color="blue", alpha=0.7, label="Data points")
        # plt.plot(x, self.predict(x), color="red", label="Regression line")
        # plt.xlabel("house area") 
        # plt.ylabel("price") 
        # plt.title("house area vs price (with Regression Line)") 
        # plt.legend()
        # plt.show()