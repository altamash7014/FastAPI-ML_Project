import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"
#input Fields

st.title = ("Life Insurance Premium Prediction")
st.markdown("Please fill in the details below to predict your life insurance premium category.")
age = st.number_input("Age", min_value=1, max_value=120, value=30)#value = 30 is deafult value
weight = st.number_input("Weight (kg)", min_value=1.0, value = 70.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value = 1.75)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value = 10.0)
city = st.text_input("City of Residence", value = "Mumbai")
smoker = st.selectbox("Are you a Smoker?", options=[True, False])
occupation = st.selectbox("Occupation", options=['private_job','government_job', 'business_owner', 'student', 'retired', 'freelancer', 'unemployed'])

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "city": city,
        "smoker": smoker,
        "occupation": occupation
    }
    response = requests.post(API_URL, json=input_data)
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Premium Category: {result['predicted_category']}")
    else:
        st.error("Error in prediction. Please try again.")