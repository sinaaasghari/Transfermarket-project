import requests
import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="Database",
    page_icon="💾",
)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_doctor = "https://assets7.lottiefiles.com/private_files/lf30_bc7loyfm.json"
lottie_doctor = load_lottieurl(lottie_url_doctor)
"------"
st.title("Design, Implementation and storage of data in the Database")
"------"
st.write("")
col1,  col2 = st.columns([10,5])
with col1:
    st.write("In this step, we used the [SQLAlchemy](https://www.sqlalchemy.org/) Python library to implement the database schema and for storing the data in it.")
    st.write("What we do at this point is storing the data in the database. For this, we use the SQLAlchemy library. It has many advantages over Python mysql connector, one of them is having Object Relational Mapping (ORM). It's a technique used in creating a 'bridge' between object-oriented programs and, in most cases, relational databases and therefore it's possible to interact with the datbase in a pythonic way rather with than pure sql queries.")
with col2:
    st_lottie(lottie_doctor, key="hello",speed=1, loop=True, quality="high", width=300,height=200)
st.write("")



st.write("")
st.markdown("""
## Steps
- • We designed an effiecient sql [schema](#schema) for storing the data.([Relations](#relations))
- • Imported and cleaned data, which was stored in `json` and `csv` files.
- • Using `SQLAlchemy` ORM, we created classes (tables) and imported data into tables (by instantiating an object of those classes and iterating data rows over them)
""")

st.markdown("")
st.markdown("")
st.markdown("")


st.markdown("## Schema")
st.markdown("")


st.markdown("")
st.markdown("##### Table: seasons")
st.markdown("""
###### Columns:
- • id (PK)
- • season_name""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: countries")
st.markdown("""
###### Columns:
- • id (PK)
- • country_name""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: leagues")
st.markdown("""
###### Columns:
- • id (PK)
- • league_name
- • country_id (Foreign Key Referrence to country table)""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: clubs")
st.markdown("""
###### Columns:
- • id (PK)
- • club_name
- • league_id (Foreign Key Referrence to league table)""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: players")
st.markdown("""
###### Columns:
- • id (PK)
- • player_name
- • date_of_birth
- • height
- • foot""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: leagues_seasonal")
st.markdown("""
###### Columns:
- • id (PK)
- • season_id (Foreign Key Referrence to season table)
- • league_id (Foreign Key Referrence to league table)
- • champion_id (Foreign Key Referrence to club table)""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: clubs_seasonal")
st.markdown("""
###### Columns:
- • id (PK)
- • season_id (Foreign Key Referrence to season table)
- • club_id (Foreign Key Referrence to club table)
- • squad_count
- • games_count
- • wins
- • draws
- • losses
- • goals_scored
- • goals recieved
- • goals differances
- • points
- • avg_age
- • avg_mkv
- • total_mkv""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: squad")
st.markdown("""
###### Columns:
- • id (PK)
- • season_id (Foreign Key Referrence to season table)
- • club_id (Foreign Key Referrence to club table)
- • player_id (Foreign Key Referrence to player table)
- • position
- • age
- • mk_value
- • agent""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: outfield_stats")
st.markdown("""
###### Columns:
- • id (PK)
- • season_id (Foreign Key Referrence to season table)
- • player_id (Foreign Key Referrence to player table)
- • total_games
- • games_played
- • goals
- • assists
- • ppg
- • yellow_cards
- • second_yellow_cards
- • red_cards""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: gk_stats")
st.markdown("""
###### Columns:
- • id (PK)
- • season_id (Foreign Key Referrence to season table)
- • player_id (Foreign Key Referrence to player table)
- • total_games
- • games_played
- • ppg
- • yellow_cards
- • second_yellow_cards
- • red_cards
- • goals_conceded
- • cleen_sheets""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: transfers")
st.markdown("""
###### Columns:
- • id (PK)
- • player_id (Foreign Key Referrence to player table)
- • season_id (Foreign Key Referrence to season table)
- • from_club (Foreign Key Referrence to club table)
- • to_club (Foreign Key Referrence to club table)
- • mk_value
- • fee""")
st.markdown("---")

st.markdown("")
st.markdown("##### Table: champions_league")
st.markdown("""
###### Columns:
- • id (PK)
- • season_id (Foreign Key Referrence to season table)
- • club_id (Foreign Key Referrence to club table)""")
st.markdown("---")
st.markdown("")
st.markdown("")

st.markdown("## Relations")
st.markdown("")
st.markdown("")
st.markdown("")
image = Image.open('transfermarkt.jpg')
st.image(image,caption='Database Schema')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("pages.css")