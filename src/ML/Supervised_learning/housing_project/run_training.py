from src.data_loader import data_loader
from src.preprocess import split_data
from src.train import train_linear_model , train_polyomial
from src.evaluate import evaluate_model
# this import is for saveing the best model
from src.save_model import save_model


# load the data

data = data_loader(r"C:\Users\Ahmed\Desktop\DEPI\DEPI Round 4\MLE SESSION TASKS\DEPI_Round4_AMIT_MLE\clean-repo\src\ML\Supervised_learning\housing_project\data\housing.csv")


# split the data
X_train , X_test , Y_train , Y_test = split_data(data , "MEDV")

# Train the models
linear_model = train_linear_model(X_train , Y_train)
poly_model = train_polyomial(X_train , Y_train)

# model Evaluation Scores
linear_results = evaluate_model(linear_model , X_test , Y_test)
poly_results = evaluate_model(poly_model , X_test , Y_test)

print("Linear: ", linear_results)
print("Polynomial: ", poly_model)

# Choose the best model
if poly_results["r2"] > linear_results["r2"]:
    best_model = poly_results
    best_name = "Polynomial"
else:
    best_model = linear_results
    best_name = "Linear"


print(f"Best model: {best_name}")

save_model(best_model , f"models/{best_name}.pkl")


