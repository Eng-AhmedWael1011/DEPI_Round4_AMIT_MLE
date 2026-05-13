from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# request Schema
from pydantic import BaseModel

# importing the prediction function from inference
from src.inference import predict_results

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    review: str

# this is App Root
@app.get("/")
def root():

    return {
        "message": "Sentiment API Running"
    }



@app.post("/predict")
def predict_sentiment(request: ReviewRequest):
    result = predict_results(request.review)
    return result





