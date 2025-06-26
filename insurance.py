from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Annotated, Literal
import pickle
import pandas as pd

app = FastAPI()

# Define the version of the model
model_version = "1.0.0"

# Load the pre-trained model
with open("Model/model.pkl", "rb") as f:
    model = pickle.load(f)

# Define the tiered cities
# These are the cities categorized into tier 1 and tier 2 for the prediction model    
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]
    height: Annotated[float, Field(..., gt=0, description="Height of the user in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the user in kg")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual income of the user in lakhs")]
    smoker: Annotated[bool, Field(..., description="Smoking status of the user")]
    city: Annotated[str, Field(..., description="City of the user")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation of the user")]
    
    
    @field_validator("city")
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi >= 30:
            return "high"
        elif self.smoker or self.bmi >= 25:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif 30 <= self.age < 60:
            return "middle-aged"
        else:
            return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        

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
    
    
@app.post("/predict")
def predict_premium(data: UserInput):
    
    input_df = pd.DataFrame([{
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
        "bmi": data.bmi,
        "lifestyle_risk": data.lifestyle_risk,
        "age_group": data.age_group,
        "city_tier": data.city_tier
    }])
    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"predicted_category": prediction})