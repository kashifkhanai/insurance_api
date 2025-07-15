from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Schema.user_input import UserInput
from Schema.prediction_response import PredictionResponse
from Model.predict import predict_output, model_version


app = FastAPI()


# Define the API endpoints
@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API is running smoothly",
        "model_version": model_version
    }
    
    
@app.post("/predict",response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
        "bmi": data.bmi,
        "lifestyle_risk": data.lifestyle_risk,
        "age_group": data.age_group,
        "city_tier": data.city_tier
    }
    
    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={"predicted_category": prediction})
    
    except Exception as e:
        
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    