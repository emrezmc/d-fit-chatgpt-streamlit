import streamlit as st
import json
from utils import *
with open('information.json', 'r') as openfile:
    # Reading from json file
    dictionary = json.load(openfile)

goal = " and ".join(dictionary['goal'])

prompt = f"I want a weekly diet program. \
            I am {dictionary['age']} years old. \
            My weight {dictionary['weight']} kilogram. \
            My height is {dictionary['height']} cm. \
            My gender is {dictionary['gender']}.\
            I want to {goal} \
            I have some health problems like {dictionary['health_problems']}\
            In addition, {dictionary['additional_info']}"


if st.button('sor'):
    #st.write(prompt)
    cevap = ask(prompt)
    st.write(cevap)