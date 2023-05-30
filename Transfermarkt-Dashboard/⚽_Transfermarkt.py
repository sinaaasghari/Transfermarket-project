import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Transfermarkt Data analysis",
    page_icon="⚽"
)



def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_flower = "https://assets3.lottiefiles.com/packages/lf20_3SQyhp.json"
lottie_flower = load_lottieurl(lottie_url_flower)
col1,col2,col3 = st.columns([1,2,1])
with col2:
    st_lottie(lottie_flower, key="hello",speed=1, loop=True, quality="medium", width=400,height=200)

"------"
st.title("Transfermarkt Data analysis Project")
"------"
st.write("")
st.subheader("Description:")
st.write('In this project we used the data from [Transfermarkt](https://www.transfermarkt.com) to do some statistical analyses and train machine learning models based on the scraped data.')
st.write('In this regard, we started the project by scraping the data, based on a database schema, which was designed to be commensurate with the analysis implementations. then after implementing and storing the data into the database, we started the statistical analysis')

st.write("")
st.subheader("Steps")
st.markdown("""
- • Scraping the required Data
- • Design, Implementation and storage of data in the Database
- • Statistical analyses
- • Machine learning model training
""")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("pages.css")