import joblib

from src.preprocessing import clean_text

model = joblib.load(
    "Models/logistic.pkl"
)

vectorizer = joblib.load(
    "Models/vectorizer.pkl"
)

def predict_results(review):

    # cleaning the text
    cleaned_review = clean_text(review)

    # vectorize the text for model requirments
    vectorized_review = vectorizer.transform([cleaned_review])

    prediction = model.predict(
        vectorized_review
    )

    probability = model.predict_proba(
        vectorized_review
    )

    if prediction == 1:
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    return {
        "review": review,
        "sentiment": sentiment,
        "confidence": probability.max()
    }

