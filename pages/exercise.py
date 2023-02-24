import json
import streamlit as st
from utils import ask
import pandas as pd
import requests

st.set_page_config(
    page_title="D-Fit",
    page_icon="🏋️",
    layout='wide'
)

loc_data = pd.read_csv('il_ilce.csv')
api_key = "AIzaSyAAQwxOV2HLs28y4ereMKYddQwIJLcoQZg"
base_url_detail = "https://maps.googleapis.com/maps/api/place/details/json"

with open('information.json', 'r') as openfile:
    dictionary = json.load(openfile)

goal = " and ".join(dictionary['goal'])

st.image('images/bmi.png')
bmi = dictionary['weight'] / (dictionary['height'] / 100) ** 2

st.write("Your bmi is " + str(round(bmi, 2)))

col1, col2, col3 = st.columns(3)
with col1:
    st.write('**How many days do you want to workout ?**')
    num_days = st.slider('*', 1, 7, 1, label_visibility="collapsed")

selected_search = dictionary['sport_type'].split()[0]
if selected_search == 'Outdoor':
        selected_sport_type = st.multiselect('Sport type', ['Basketball', 'Swimming', 'Soccer', 'Tennis', 'Sailing', 'Running'])

if st.button('Give my exercise plan'):
    with st.spinner(text="In progress..."):
        prompt = f"""
                Can you give me workout program that monday to sunday with rest days for {dictionary['sport_type']},
                I'm {dictionary['level_type']}  give reps with their set please.
                Please just give me the program, not write me anything without program.
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
                """
        if selected_sport_type:
            prompt = prompt + f'I want only {selected_sport_type} program. Give me the program only for {num_days} days.'
        cevap = ask(prompt)
        st.write(cevap)

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
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            'input' : query,
            'inputtype': 'textquery',
            'fields': 'name,geometry',
            'key' : api_key
        }
        response = requests.get(url, params=params)
        result = response.json()
        loc = result["candidates"][0]['geometry']['location']
        lat, lng = loc['lat'], loc['lng']

        url_near = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params_near = {
            'location': f"{lat} {lng}",
            'keyword': selected_sport_type,
            'type': 'gym|health|establishment',
            'rankby': 'distance',
            'key': api_key
        }
        response = requests.get(url_near, params=params_near)

        near_result = response.json()
        results = near_result['results'][:5]
        map_links = []
        for result in results:
            params_detail = {
            "place_id" : result["place_id"],
            'field' : "url",
            "key" : api_key
            }
            detail_response = requests.get(base_url_detail, params = params_detail)
            detail = detail_response.json()
            map_links.append(detail["result"]["url"])
            
        for i, res in enumerate(results):
            column_1, column_2, column_3 = st.columns(3)
            with column_1:
                st.write(res["name"])
            with column_2:
                st.write(map_links[i])
            with column_3:
                st.write(res["rating"])
