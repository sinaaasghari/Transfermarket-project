import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests

st.set_page_config(
    page_title="Machine Learning",
    page_icon="🤖",
)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url_download = "https://assets3.lottiefiles.com/packages/lf20_kUtZCR7Zyk.json"

lottie_download = load_lottieurl(lottie_url_download)
st.title('Machine Learning')

st_lottie(lottie_download, key="hello",speed=1, loop=True, quality="medium", width=700,height=400)



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("pages.css")
