import json
import streamlit as st
from utils import ask, findplace_text, near_search, get_detail_place, main_button, diet_button,load_lottieurl
import pandas as pd
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="D-Fit",
    page_icon=":weight_lifter:",
    layout='wide'
)

loc_data = pd.read_csv('il_ilce.csv')

with open('information.json', 'r') as openfile:
    dictionary = json.load(openfile)


bmi = dictionary['weight'] / (dictionary['height'] / 100) ** 2


#navi_url = "https://assets6.lottiefiles.com/private_files/lf30_A6ckDx.json"
with open('images/navi.json', 'r') as openfile:
    navi_json = json.load(openfile)

st.markdown("<h1 style='text-align: left; color: blue;'> BMI & Exercise Plan</h1>", unsafe_allow_html=True)

if  dictionary["gender"] == "Male":
    st.image('images/bmi_man.jpg', width=700)
else:
    st.image('images/bmi_woman.jpg', width=700)


if bmi < 18.5:
    st.write(f'**Your BMI is: {str(round(bmi, 2))}. Your BMI is underweight.**')
elif (18.5 <= bmi < 25):
    st.write(f'**Your BMI is: {str(round(bmi, 2))}. Your BMI is normal.**')
elif (25 <= bmi < 30):
    st.write(f'**Your BMI is: {str(round(bmi, 2))}. Your BMI is overweight.**')
elif (30 <= bmi < 35):
    st.write(f'**Your BMI is: {str(round(bmi, 2))}. Your BMI is obese.**')
else:
    st.write(f'**Your BMI is: {str(round(bmi, 2))}. Your BMI is extremely obese.**')


st.write('&nbsp;',unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
with col1:
    st.write('**How many days do you want to workout ?**')
    num_days = st.slider('*', 1, 7, 1, label_visibility="collapsed")

selected_search = dictionary['sport_type'].split()[0]
selected_sport_type = None
if selected_search == 'Outdoor':
        selected_sport_type = st.multiselect('Sport type', ['Basketball', 'Swimming', 'Soccer', 'Tennis', 'Sailing', 'Running'])


if st.button('Give my exercise plan'):
    with st.spinner(text="Creating your exercise plan..."):
        goal = " and ".join(dictionary['goal'])
        prompt = f"""
                Based on my personal information, can you give me a workout schedule table with rest days from Monday 
                to Sunday for the {dictionary['sport_type']}? I am a {dictionary['level_type']}, 
                and please give me sets of reps. Each day should begin with a warm-up and end with a cool-down exercise. 
                I am {dictionary['age']} years old and {dictionary['gender']}. 
                My weight is {dictionary['weight']}  kilos, and my height is {dictionary['height']} cm. 
                I want to {goal}. Please give me the {num_days}-days program, do not write me anything but the program content. 
                The program should include at least 6 movements per day, 
                and these movements should work one large muscle group and one small muscle group per day. 
                Please do not give it as a lower, upper, full-body program. 
                The program should be based on a large muscle group-small muscle group daily.
                """
        
        if dictionary['additional_info'] != "":
            prompt = prompt + f"In addition, {dictionary['additional_info']} "

        if dictionary['health_problems'] != "":
            prompt += f"I have some health problems like {dictionary['health_problems']}"

        if selected_sport_type:
            prompt = prompt + f'I want only {selected_sport_type} program.'

        cevap = ask(prompt)
        st.write(cevap)

st.write('&nbsp;',unsafe_allow_html=True)

if selected_search != 'Home':

    st.write('**Find closest sport center:**')

    column_1, column_2, column_3 = st.columns(3, gap='medium')
    with column_1:
        sehirler = loc_data.il.unique().tolist()
        selected_city = st.selectbox("City", sehirler)
    with column_2:
        ilceler = loc_data[loc_data.il == selected_city]['ilçe'].unique().tolist()
        selected_county = st.selectbox("District", ilceler)
    with column_3:
        mahalleler = loc_data[(loc_data.il == selected_city) & (loc_data['ilçe']== selected_county)]["Mahalle"].unique().tolist()
        selected_mahalle = st.selectbox('Neighborhood', mahalleler)

    query = selected_city + selected_county + selected_mahalle

    if st.button('Show'):
        lat, lng = findplace_text(query)
        near_result = near_search(lat, lng, selected_sport_type)
        results = near_result['results'][:5]
        map_links = [get_detail_place(result["place_id"]) for result in results]
        for i, res in enumerate(results):
            column_1, column_2, column_3 = st.columns(3)
            with column_1:
                st.write(res["name"])
            with column_2:
                st.write(map_links[i])
            with column_3:
                st.write(res["rating"])
    
    st_lottie(navi_json, key="navi", height= 200, width=200)


col_1, col_2 = st.columns(2)
with col_1:
    main_button()
with col_2:
    diet_button()