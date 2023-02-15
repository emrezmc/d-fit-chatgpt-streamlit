import openai
import streamlit as st
from streamlit.components.v1 import html
import json

def diet_button(dictionary):
    if st.button("Give Diet Program"):
    # Set the query parameters to include the name
        write_json(dictionary)
        nav_page('diet')

def exercise_button(dictionary):
    if st.button("Give Exercise Program"):
    # Set the query parameters to include the name
        write_json(dictionary)
        nav_page('exercise')

def write_json(dictionary):
    json_object = json.dumps(dictionary, indent=4)
    
    # Writing to sample.json
    with open("information.json", "w") as outfile:
        outfile.write(json_object)

def ask(question):
    openai.api_key = ('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')
    response = openai.Completion.create(
        prompt=question,
        model="text-davinci-003",
        temperature=0.3,
        max_tokens=1000,
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