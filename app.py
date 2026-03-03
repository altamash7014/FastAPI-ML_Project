from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
# from typing import Literal, Annotated
from typing import Literal, Annotated, ClassVar
import pickle
import pandas as pd

# import the ml model
with open('a3model.pkl', 'rb') as f: #rb means read binary
    model = pickle.load(f)

# created fastapi object
app = FastAPI()


# now we will create pydantic model to validate the incoming data and also to create new features as we did in the notebook
# to validate incoming data,we will create a pydantic model
class UserInput(BaseModel):
    age: Annotated[int, Field(...,gt=0, description="Age of user")]  #... means required field, gt means greater than
    weight: Annotated[float, Field(...,gt=0, description="Weight must be greater than 0")]
    height: Annotated[float, Field(...,gt=0, lt = 2.5,description="Height must be in meters and less than 2.5")]
    income_lpa: Annotated[float, Field(...,gt=0, description="Annual income in lakhs per annum must be greater than 0")]
    city: Annotated[str, Field(...,description="City of residence")]
    occupation: Annotated[Literal['salaried', 'self-employed', 'student', 'retired'], Field(...,description="Occupation of the user")]
    smoker: Annotated[bool, Field(...,description="Whether the user is a smoker or not")]


#now we have to create new features as we created in notebook like bmi with hellp of weight and height
# we can use computed_field to create new features
# we will create a computed field for bmi
    @computed_field
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    # lifestyle_risk is a computed field based on occupation and smoker status
    @computed_field 
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 30:
            return 'medium'
        else:
            return 'low'
        
#city tier is a computed field based on city of residence
    tier_1_cities: ClassVar[list[str]] = [
        "Mumbai", "Delhi", "Bangalore", "Chennai",
        "Kolkata", "Hyderabad", "Pune"
    ]

    tier_2_cities: ClassVar[list[str]] = [
        "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
        "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
        "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
        "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
        "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
        "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
    ]

    @computed_field
    # @property
    def city_tier(self) -> str:
        if self.city in self.tier_1_cities:
            return 'Tier 1'
        elif self.city in self.tier_2_cities:
            return 'Tier 2'
        else:
            return 'Tier 3'
        
    @computed_field
    # @property
    def age_group(self)-> str:
        
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"


# Pydantic model is created`
# now we will create an endpoint to receive the data and make predictions
# @app.post("/predict")
# def predict_premium(data: UserInput):

    # input_df = pd.DataFrame([{
    #     'bmi': data.bmi,
    #     'age_group': data.age_group,
    #     'lifestyle_risk': data.lifestyle_risk,
    #     'city_tier': data.city_tier,
    #     'income_lpa': data.income_lpa,
    #     'occupation': data.occupation
    # }]) # convert the pydantic model to a dataframe  

    # prediction = model.predict(input_df)[0] # make prediction using the model
    # return JSONResponse(status_code=200, content={"predicted_premium": prediction[0]}) # return the prediction as a json response
# @app.post("/predict")
# def predict_premium(data: UserInput):

#     input_df = pd.DataFrame([{
#         'bmi': data.bmi,
#         'age_group': data.age_group,
#         'lifestyle_risk': data.lifestyle_risk,
#         'city_tier': data.city_tier,
#         'income_lpa': data.income_lpa,
#         'occupation': data.occupation
#     }])

#     print(input_df)  # ADD THIS

# @app.post('/predict')
# def predict_premium(data: UserInput):

#     input_df = pd.DataFrame([{
#         'bmi': data.bmi,
#         'age_group': data.age_group,
#         'lifestyle_risk': data.lifestyle_risk,
#         'city_tier': data.city_tier,
#         'income_lpa': data.income_lpa,
#         'occupation': data.occupation
#     }])

#     prediction = model.predict(input_df)[0]

#     return JSONResponse(
#         status_code=200,
#          content={'predicted_category': str(prediction)}
#     )
@app.post('/predict')
def predict_premium(data: UserInput):

    try:
        input_df = pd.DataFrame([{
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }])

        print(input_df)  # DEBUG
        prediction = model.predict(input_df)[0]
        print("Prediction:", prediction)

        return {
            "predicted_category": str(prediction)
        }

    except Exception as e:
        return {"error": str(e)}
        # import streamlit as st
        # import requests

        # API_URL = ""
        # st.title("Insurance Premium Category Predictor")
        # st.markdown("Enter the details below to predict the insurance premium category.")
        # #input Fields
        # age = st.number_input("Age", min_value=1, max_value=120, value=30)
        # weight = st.number_input("Weight (kg)", min_value=1.0, value = 70.0)
        # height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value = 1.75)
        # income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value = 10.0)
        # city = st.text_input("City of Residence", value = "Mumbai")
        # smoker = st.selectbox("Are you a Smoker?", options=[True, False])
        # occupation = st.selectbox("Occupation", options=['private_job','government_job', 'business_owner', 'student', 'retired', 'freelancer', 'unemployed'])
