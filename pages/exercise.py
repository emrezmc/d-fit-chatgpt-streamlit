import streamlit as st
import json
from utils import *
import pandas as pd

st.set_page_config(
    page_title="D-Fit",
    page_icon="🏋️",
    layout='wide'
)

with open('information.json', 'r') as openfile:
    dictionary = json.load(openfile)

goal = " and ".join(dictionary['goal'])

st.image('images/bmi.png')
bmi = dictionary['weight'] / (dictionary['height'] / 100) ** 2

st.write("Your bmi is " + str(round(bmi, 2)))

col1, col2, col3 = st.columns(3)
with col1:
    st.write('**How many days do you want to workout ?**')
    num_days = st.slider('', 1, 7, 1, label_visibility="collapsed")
    
if st.button('Give my exercise plan'):
    with st.spinner(text="In progress..."):
        prompt = f" Can you give me workout program that monday to sunday for {dictionary['sport_type']} \
                Please just give me the program, not write me anything without program.Next to each move give a youtube link showing the move. \
                I want to workout {num_days} days in a week. \
                I am {dictionary['age']} years old. \
                My weight {dictionary['weight']} kilogram. \
                My height is {dictionary['height']} cm. \
                My gender is {dictionary['gender']}.\
                I want to {goal}. \
                I have some health problems like {dictionary['health_problems']}.\
                In addition, {dictionary['additional_info']}."
        cevap = ask(prompt)
        st.write(cevap)

