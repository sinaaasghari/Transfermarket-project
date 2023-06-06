import requests
import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="Scraping the required Data",
    page_icon="🥣",
)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_doctor = "https://assets1.lottiefiles.com/packages/lf20_DbCYKfCXBZ.json"
lottie_doctor = load_lottieurl(lottie_url_doctor)
"------"
st.title("Scraping the required Data")
"------"
st.write("")
col1,  col2 = st.columns([10,5])
with col1:
    st.write("In this step, we used the [Requests](https://requests.readthedocs.io/en/latest/) and [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) Python libraries to extract the required data.")
    st.write("In this regard, we first developed an outline for the required data, based on our statistics and machine learning tasks. Then we designed a suitable database schema for it. Finally, based on the database tables, we divided the tasks among the group members, and started extracting the data.")
with col2:
    st_lottie(lottie_doctor, key="hello",speed=1, loop=True, quality="medium", width=300,height=200)
st.write("")



st.write("")
st.subheader("Steps")
st.markdown("""
- • Scraping the seasons and countries data.
- • Scraping the leagues data based on seasons and countries and unique information for each league.
- • Scraping the clubs data based on seasons and leagues and unique information for each club.
- • Scraping the players data based on seasons and clubs and unique information (performances) for each player.
- • Scraping the transfer data for each of the players.
- • Scraping the data of the clubs' appearance in the 2021 Champions League.
""")
st.write("")

st.write("")
image = Image.open('about.jpg')
st.image(image,caption='Beautiful Soup')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("pages.css")