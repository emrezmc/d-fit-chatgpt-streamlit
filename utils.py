import json
import openai
import requests
import streamlit as st

from streamlit.components.v1 import html


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def save_button(dictionary):
    if st.button('Save Info'):
        write_json(dictionary)

def main_button():
    if st.button('Main page'):
        nav_page('')

def diet_button():
    if st.button("Give Diet Program"):
        #write_json(dictionary)
        nav_page('Diet')

def exercise_button():
    if st.button("Give Exercise Program"):
        #write_json(dictionary)
        nav_page('Exercise')

def write_json(dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open("information.json", "w") as outfile:
        outfile.write(json_object)

def ask(question):
    openai.api_key = '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'
    response = openai.Completion.create(
        prompt=question,
        model="text-davinci-003",
        temperature=0.3,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    answer = response.choices[0].text.strip()
    return answer

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

def findplace_text(query):
    api_key = "AIzaSyAAQwxOV2HLs28y4ereMKYddQwIJLcoQZg"
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
    return lat, lng

def near_search(lat, lng, selected_sport_type):
    api_key = "AIzaSyAAQwxOV2HLs28y4ereMKYddQwIJLcoQZg"
    url_near = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params_near = {
            'location': f"{lat} {lng}",
            'keyword': selected_sport_type,
            'type': 'gym|health|establishment',
            'rankby': 'distance',
            'key': api_key
        }
    response = requests.get(url_near, params=params_near)
    return response.json()

def get_detail_place(place_id):
    api_key = "AIzaSyAAQwxOV2HLs28y4ereMKYddQwIJLcoQZg"
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params_detail = {
            "place_id" : place_id,
            'field' : "url",
            "key" : api_key
            }
    detail_response = requests.get(url, params = params_detail)
    detail = detail_response.json()
    return detail["result"]["url"]
