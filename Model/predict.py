import pickle
import pandas as pd


# Define the version of the model
model_version = "1.0.0"

# Load the pre-trained model
with open("Model/model.pkl", "rb") as f:
    model = pickle.load(f)
    
def predict_output(user_input: dict):
    
    input_df = pd.DataFrame(user_input)
    
    output = model.predict(input_df)[0]
    
    return output


