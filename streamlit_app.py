import time
import json
import requests
from pytz import timezone 
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components



with st.sidebar: 
    start_location = st.selectbox(
        "Select your current location",
        ["Leugenestrasse,Biel,Bern,Switzerland", "40 W. Switzerland,Lausanne,Switzerland"]
    )

    dest_location = st.selectbox(
        "Select your next location",
        ["40 W. Switzerland,Lausanne,Switzerland", "Leugenestrasse,Biel,Bern,Switzerland"]
    )

custom_css = """
<style>
.bottom-right {
    position: fixed;
    bottom: 0;
    right: 0;
    padding: 10px;
    color: blue;
    font-size: 16px; /* Adjust the font size as needed */
    background-color: rgba(255, 255, 255, 0.8); /* Optional: adds a background color with transparency */
}
</style>
"""
# Inject the CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(
    '''
    <div class="bottom-right">
        Powered by <a href="https://www.ibm.com/products/watsonx-ai" target="_blank">watsonx.ai</a>
    </div>
    ''',
    unsafe_allow_html=True
)

if st.sidebar.button("Get routes"):
    with st.spinner('**fetching routes.....**'):
        payload = {
                "freight_order_number": "6100000501",
                "route_stops": [
                    {"stop": 1, "latitude": 0, "longitude": 0, "name": start_location},
                    {"stop": 2, "latitude": 0, "longitude": 0, "name": dest_location}
                                ]
                } 
        
        response = requests.post("https://routeplanapp.1b4zg4753bwe.us-south.codeengine.appdomain.cloud/processroutedata", 
                                 data=json.dumps(payload),
                                 headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            jsondata = response.json()
            maindata = jsondata["output"]
            for each_leg in maindata:
                all_routes_map = each_leg['map_all_html']
                llm_response = each_leg['recommendation']
                best_route_map = each_leg['map_html']
                

                st.subheader('All available routes are...', divider='rainbow')
                components.html(all_routes_map, height=450)

                st.subheader('Best route recommended by LLM ', divider='rainbow')
                st.info(llm_response)

                st.subheader('Best route', divider='rainbow')
                components.html(best_route_map, height=450)
        else:
            st.info("No responce received")