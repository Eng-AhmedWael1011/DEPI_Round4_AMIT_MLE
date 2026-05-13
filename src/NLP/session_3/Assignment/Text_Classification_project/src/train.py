import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from src.preprocessing import clean_text
from src.features import create_vectorizer , Word2VecVectorizer

# step1 load_data

print('Loading Data....')

df = pd.read_csv(
    "Data/IMDB Dataset.csv"
)

print('Data loaded Successfully')


# encoding the sentiment

print('encoding and cleaning....')

df['sentiment'] = df['sentiment'].map({
    'positive': 1,
    'negative': 0
})

df['sentiment'].astype(int)

# cleaning the text

df['cleaned_review'] = df['review'].apply(clean_text)

# creating the vectorizer using the tf-idf vectorizer

print('Done.')
print('Vectorizing data...')

vectorizer = Word2VecVectorizer()

# devloping the tokens for training
X = vectorizer.fit_transform(df['cleaned_review'])
y = df['sentiment']

print('Done.')
print('Training model.')

X_train , X_test , y_train , y_test = train_test_split(X , y , test_size=0.25 , random_state=42)

model = LogisticRegression()
model.fit(X_train , y_train)

print('done.')

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Accuracy: {accuracy:.4f}")

print('Saving model and vectorzier...')

# Saving the model
joblib.dump(
    model,
    "Models/logistic.pkl"
)

# Saving the vectorizer
joblib.dump(
    vectorizer,
    "Models/vectorizer.pkl"
)

joblib.dump(X_test, 'Models/X_test.pkl')
joblib.dump(y_test, 'Models/y_test.pkl')

joblib.dump(X_train, 'Models/X_train.pkl')
joblib.dump(y_train, 'Models/y_train.pkl')

print('Done & finished Successfully')