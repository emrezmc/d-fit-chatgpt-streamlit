import streamlit as st
from utils import *


st.set_page_config(
    page_title="D-Fit",
    page_icon="🏋️",
)




st.markdown("<h1 style='text-align: center;background-color: #0074D9;'>D-Fit </h1>", unsafe_allow_html=True)

st.title("Personal Informations")

age = st.number_input("Enter your age", value=18, min_value=1, max_value=80)
weight = st.number_input("Enter your weight (in kg)", value=50.0, min_value=1.0, max_value=500.0, step=0.1) 
height = st.number_input("Enter your height (in cm)", value=160, min_value=1, max_value=300) 
gender = st.selectbox("Select your gender", options=["Male", "Female", "Other"])
sport_type = st.selectbox("Select your workout place", options=["Home Workout 🧘", "Gym Workout 🏋️ ", "Outdoor 🚣‍♀️ 🏊"])

goal = st.multiselect("What is your goal ? ", options=["Lose Weight",
"Gain Weight" ,
"Gain Muscle ",
"Improve Flexibility",
"Weight Stability"])

health_problems = st.text_input("Your health problems ? Ex. allergens, diabet, disabilities... (You can leave it blank)")
additional_info = st.text_input("Your additional desires ex. ")


dictionary = {'age':age,
'weight':weight,
'height':height,
'gender': gender,
'sport_type':sport_type,
'goal': goal,
'health_problems': health_problems,
'additional_info': additional_info}


#bmi = weight / (height/100)**2
submit_button(dictionary)



