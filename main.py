import json
import streamlit as st
from utils import diet_button, exercise_button, save_button

st.set_page_config(
    page_title="D-Fit",
    page_icon=":weight_lifter:",
    layout='wide'
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 250px;
        margin-left: -250px;
    }
    """,
    unsafe_allow_html=True,
)

try:
    with open('information.json', 'r') as openfile:
        dictionary = json.load(openfile)
        age = dictionary['age']
        weight = dictionary['weight']
        height = dictionary['height']

        if dictionary['gender'] == 'Female':
            gender = 0
        elif dictionary['gender'] == 'Male':
            gender = 1
        else:
            gender = 2
        
        sport_type_filtered = dictionary['sport_type'].split()[0]
        if sport_type_filtered == 'Home':
            sport_type = 0
        elif sport_type_filtered == 'Gym':
            sport_type = 1
        else:
            sport_type = 2
        level_type_filtered = dictionary['level_type'].split()[0]
        if level_type_filtered == 'Beginner':
            level_type = 0
        elif level_type_filtered == 'Intermediate':
            level_type = 1
        else:
            level_type = 2
        
        goal = dictionary['goal']
        health_problems = dictionary['health_problems']
        additional_info = dictionary['additional_info']
except:
    age = 18
    weight = 50.0
    height = 160
    gender = 0
    sport_type = 0
    level_type = 0
    goal = None
    health_problems = ''
    additional_info = ''

st.markdown("<h1 style='text-align: center;font-size: 60px'>D-Fit </h1>",
            unsafe_allow_html=True)
#st.title("Personal Informations")
st.markdown("<h2 style=''>Personal Informations </h2>",
            unsafe_allow_html=True)

col_1, col_2, col_3 = st.columns(3, gap='medium')
with col_1:
    input_age = st.number_input("Enter your age", value=age, min_value=1, max_value=80)
    input_gender = st.selectbox("Select your gender", options=["Female", 'Male', "Other"], index=gender)
with col_2:
    input_weight = st.number_input("Enter your weight (in kg)", value=weight,
            min_value=1.0, max_value=500.0, step=0.5)
    input_sport_type = st.selectbox("Select your workout place",
                options=["Home Workout 🧘", "Gym Workout 🏋️ ", "Outdoor Workout 🚣‍♀️ 🏊"], index=sport_type)
with col_3:
    input_height = st.number_input("Enter your height (in cm)", value=height, min_value=1, max_value=300)
    input_goal = st.multiselect("What is your goal ? ", options=["Lose Weight",
                    "Gain Weight" ,
                    "Gain Muscle ",
                    "Improve Flexibility",
                    "Weight Stability"], default=goal)

input_level_type = st.selectbox("Choose your level ",
                options=["Beginner  (I just started doing sports or haven't been doing sports for a long time and I don't have an athlete background.)",
                          "Intermediate (It has always been sports in some way in my life. I exercise, although not regularly.) ", 
                          "Advanced (I have been playing sports for a long time or I am a professional athlete in a sport)"], index= level_type)

input_health_problems = st.text_input("Your health problems ? \
                    Ex. allergens, diabet, disabilities... (You can leave it blank)", value = health_problems)
input_additional_info = st.text_input("Your additional desires ex. ", value=additional_info)


dictionary = {'age':input_age,
'weight':input_weight,
'height':input_height,
'gender': input_gender,
'sport_type':input_sport_type,
'goal': input_goal,
'health_problems': input_health_problems,
'additional_info': input_additional_info,
'level_type': input_level_type}


col1, col2, col3 = st.columns(3, gap='large')
with col1:
    save_button(dictionary)
with col2:
    diet_button()
with col3:
    exercise_button()
    