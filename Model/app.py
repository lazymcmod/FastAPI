from fastapi import FastAPI
from Model.predict import predict_output
from Schema.user_input import UserInput
from Schema.prediction_response import PredictionResponse


app = FastAPI()


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(user_input: UserInput):

    result = predict_output(user_input.model_dump())

    return result