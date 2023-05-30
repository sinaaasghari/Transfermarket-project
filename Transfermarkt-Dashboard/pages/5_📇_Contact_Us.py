import streamlit as st
import base64
from streamlit.components.v1 import html


st.set_page_config(
    page_title="Contact us",
    page_icon="👨‍⚕️",
)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")
