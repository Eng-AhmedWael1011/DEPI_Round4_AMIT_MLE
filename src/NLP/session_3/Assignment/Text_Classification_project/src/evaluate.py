import joblib
from sklearn.metrics import accuracy_score,classification_report, confusion_matrix, f1_score , roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns


X_test = joblib.load('Models/X_test.pkl')
y_test = joblib.load('Models/y_test.pkl')


model = joblib.load('Models/logistic.pkl')

def plot_confusion_matrix():

    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test , y_pred)

    return sns.heatmap(cm , annot=True)


def plot_roc_curve():
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr , thresholds = roc_curve(y_test, y_prob)

    auc_score = roc_auc_score(y_test, y_prob)
    print(auc_score)

    plt.figure(figsize=(8,6))

    plt.plot(
        fpr,
        tpr,
        label=f"AUC = {auc_score:.4f}"
    )

    # random classifier line
    plt.plot(
        [0,1],
        [0,1],
        linestyle='--'
    )

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")

    plt.title("ROC Curve - Logistic Regression")

    plt.legend()


plot_confusion_matrix()
plot_roc_curve()

plt.show()