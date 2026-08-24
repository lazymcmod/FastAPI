from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
from Schema.user_input import UserInput
from Model.predict import predict_output,model,MODEL_VERSION

app = FastAPI()

# human readable
@app.get('/')
def home():
    return {'message': 'Insurance Premium Predictor API'}

# machine readable
@app.get('/health')
def health():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'Model_loaded': model is not None
    }

@app.post('/predict')
def predict_premium(data: UserInput):

    user_input = ([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation

    }])

    prediction = predict_output(user_input)
    return {
        "predicted_category": str(prediction[0])
    }