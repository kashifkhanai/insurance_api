import pickle
import pandas as pd


# Define the version of the model
model_version = "1.0.0"

# Load the pre-trained model
with open("Model/model.pkl", "rb") as f:
    model = pickle.load(f)
    
# Define the class labels   
class_labels = model.classes_.tolist()

# Function to predict the output based on user input
def predict_output(user_input: dict):
    
    input_df = pd.DataFrame([user_input])
    
    # perdict the class 
    predicted_class = model.predict(input_df)[0]
    
    # get probability of the predicted class
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)
    
    # creating Maping :{class_name : confidence}
    class_probs = dict(zip(class_labels,map(lambda x: round(x, 4), probabilities)))
    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }
    
    r


