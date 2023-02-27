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


navi_url = "https://assets6.lottiefiles.com/private_files/lf30_A6ckDx.json"

st.markdown("<h1 style='text-align: center; color: blue;'> BMI & Exercise Plan</h1>", unsafe_allow_html=True)

if  dictionary["gender"] == "Male":
    st.image('images/bmi_man.jpg', width=700)
else:
    st.image('images/bmi_woman.jpg', width=700)



st.write("Your bmi is " + str(round(bmi, 2)))

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
                Can you give me workout program table that monday to sunday with rest days for {dictionary['sport_type']},
                I'm {dictionary['level_type']}  give reps with their set please.
                Please just give me the {num_days} days program, not write me anything without program.
                Paying attention to regional muscle groups (just working one major muscle and one minor muscle group per day)
                Each day begins with warm-up exercises. 
                I want to workout {num_days} days in a week. 
                I am {dictionary['age']} years old.
                My weight {dictionary['weight']} kilogram.
                My height is {dictionary['height']} cm.
                My gender is {dictionary['gender']}.
                I want to {goal}.
                I have some health problems like {dictionary['health_problems']}.
                In addition, {dictionary['additional_info']}.
                As I said earlier, I want {num_days} days workout plan, so give me exactly the same number of workout routine please.
                """
        if selected_sport_type:
            prompt = prompt + f'I want only {selected_sport_type} program. Give me the program only for {num_days} days.'
        cevap = ask(prompt)
        st.write(cevap)

if selected_search != 'Home':
    st.write('**Find closest sport center:**')


    navi = load_lottieurl(navi_url)
    st_lottie(navi, key="navi", height= 400, width=600)

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

col_1, col_2 = st.columns(2)
with col_1:
    main_button()
with col_2:
    diet_button()