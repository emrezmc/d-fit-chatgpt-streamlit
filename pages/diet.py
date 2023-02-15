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

prompt = f"I want a monday to sunday weekly diet program, only give me program don't give any advice. \
            I am {dictionary['age']} years old. \
            My weight {dictionary['weight']} kilogram. \
            My height is {dictionary['height']} cm. \
            My gender is {dictionary['gender']}.\
            I want to {goal} \
            I have some health problems like {dictionary['health_problems']}\
            In addition, {dictionary['additional_info']}"

with st.spinner(text="In progress..."):
    cevap = ask(prompt)
    menu_dict = {}
    for day_menu in cevap.split('\n\n'):
        lines = day_menu.split('\n')
        day = lines[0].split(':')[0]
        meals = {}
        for line in lines[1:]:
            meal, menu = line.split(': ')
            meals[meal] = menu
        menu_dict[day] = meals

    st.table(pd.DataFrame(menu_dict))
