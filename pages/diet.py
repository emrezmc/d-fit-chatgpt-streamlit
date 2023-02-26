import json
import streamlit as st
from utils import ask, main_button, exercise_button, load_lottieurl
import pandas as pd
from streamlit_lottie import st_lottie

lottie_diet_url = "https://assets8.lottiefiles.com/packages/lf20_qxjbnrlu.json"
lottie_diet = load_lottieurl(lottie_diet_url)

st.set_page_config(
    page_title="D-Fit",
    page_icon=":cooking:",
    layout='wide'

)
def get_plan(prompt):
    with st.spinner('Your diet plan is creating...'):
            cevap = ask(prompt)
            cevap = "Monday" + cevap.split('Monday',1)[1]
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

try:
    with open('information.json', 'r') as openfile:
        dictionary = json.load(openfile)
except:
    pass # BURAYA uyarı eklencek kod yukarı alıncak.
    #st.write()

goal = " and ".join(dictionary['goal'])
prompt = f"I want a monday to sunday weekly diet program, only give me diet program don't give any advice.\
            In addition, please write amounts of foods users sould eat next to them. \
            I am {dictionary['age']} years old. \
            My weight {dictionary['weight']} kilogram. \
            My height is {dictionary['height']} cm. \
            My gender is {dictionary['gender']}.\
            I want to {goal}"

if dictionary['additional_info'] != "":
     prompt = prompt + f"In addition, {dictionary['additional_info']} "

if dictionary['health_problems'] != "":
     prompt += f"I have some health problems like {dictionary['health_problems']}"

#st.write(dictionary)
#st.write(prompt)
st_lottie(lottie_diet, key="diet", height= 600, width=800)

get_plan(prompt)
