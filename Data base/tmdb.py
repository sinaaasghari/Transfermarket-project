from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float, Numeric

from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

import json
import pandas as pd

#--------------------fuctions to clean and debug the data------------------------

def palyer_height_clean(ph):
    if pd.isna(ph):
        return None
    else:
        ph = float(ph.replace(',', '.'))
        return ph

def mkv_cleaner(mkv):
    if mkv == 'None':
        return None
    else:
        return mkv

def season_cleaner(seas):
    if seas[-2] == '9':
        seas = '19' + seas[-2:]
    return int(seas)
def mkv_clean(mkv):
    if pd.isna(mkv):
        return None
    else:
        return mkv
    
def age_clean(age):
    if pd.isna(age):
        return None
    else:
        return age

def performance_clean(inp):
    try:
        inp = int(inp)
    except:
        try:
            inp= float(inp)
        except:
            inp = None
    return inp



#---------------------------Importing the scraped data and cleaning it----------------------------

#season, countries, leagues
with open("SCL.json", "r") as file:
    import_data = json.load(file)

seasons = import_data[0]
countries = import_data[1]
leagues = import_data[2]
countries.append({'country_id': '404', 'country_name': 'Not Recorded'})

unique_leagues = []
for lg in leagues:
    if not any(individual['league_id'] == lg['league_id'] for individual in unique_leagues):
        unique_leagues.append(dict(league_id= lg['league_id'], name= lg['name'], country_id= lg['country_id']))
unique_leagues.append({'league_id': 'Nrc', 'name': 'Not Recorded', 'country_id': '404'})

#clubs
with open("Clubs_and_ClubsBySeasons.json", "r") as file:
    club_data = json.load(file)

clubs = club_data[0]
clubs_se = pd.read_csv('seasonal_clubs_with_performances.csv')

#players
players_df = pd.read_json("Player_json.json")
unique_players_df = players_df.drop_duplicates(subset='player_id', keep='last')[['player_id', 'Name', 'Date_of_birth', 'Height', 'Foot']]

#palyers stats
with open("Player.json", "r") as file:
    out_stat = json.load(file)

with open("GK.json", "r") as file:
    gk_stat = json.load(file)

#transfers
with open("transfer_stats.json", "r") as file:
    transfers = json.load(file)

for item in transfers:
    if not any(individual['club_id'] == item['from_id'] for individual in clubs):

        club_id = item['from_id']
        clubs.append({'club_id': club_id, 'league_id': 'Nrc', 'name': item['from_name']})

    if not any(individual['club_id'] == item['to_id'] for individual in clubs):

        club_id = item['to_id']
        clubs.append({'club_id': club_id, 'league_id': 'Nrc', 'name': item['to_name']})

#Champions_League
with open("Champions_league.json", "r") as file:
    chamions_league = json.load(file)

#--------------------------------------------Creating engine and Database----------------------------------------

# Creating a URL and an engine (connection):

url_object = URL.create(
    "mysql+mysqlconnector",
    username="Arsalan_quera",
    password="Quera402",
    host="localhost",
)

engine = create_engine(url_object)

# Creating the database of tranfermarkt top movies:

DB_NAME = 'transfermarkt'

with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
    conn.execute(text(f"USE {DB_NAME}"))

# Creating the Base calss over DeclarativeBase calss:

class Base(DeclarativeBase):
    pass



# Creating a URL and an engine (connection) again with specified database:

url_object = URL.create(
    "mysql+mysqlconnector",
    username="Arsalan_quera",
    password="Quera402",
    host="localhost",
    database=DB_NAME
)

engine = create_engine(url_object)

# Creating classes over Base class (Creating the desired tables):
class Season(Base):
    __tablename__ = "seasons"
    
    id = mapped_column(Integer, primary_key=True)
    season_name = mapped_column(String(8))


class Country(Base):
    __tablename__ = "countries"
    
    id = mapped_column(Integer, primary_key=True)
    country_name = mapped_column(String(16))


class League(Base):
    __tablename__ = "leagues"
    id = mapped_column(String(4), primary_key=True)
    league_name = mapped_column(String(32))
    country_id = mapped_column(Integer, ForeignKey('countries.id'))


class Club(Base):
    __tablename__ = "clubs"
    id = mapped_column(Integer, primary_key=True)
    club_name = mapped_column(String(32))
    league_id = mapped_column(String(4), ForeignKey('leagues.id'))


class LeagueSeasonal(Base):
    __tablename__ = "leagues_seasonal"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id = mapped_column(Integer, ForeignKey('seasons.id'))
    league_id = mapped_column(String(4), ForeignKey('leagues.id'))
    champion_id = mapped_column(Integer, ForeignKey('clubs.id'))


class ClubSeasonal(Base):
    __tablename__ = "clubs_seasonal"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id = mapped_column(Integer, ForeignKey('seasons.id'))
    club_id = mapped_column(Integer, ForeignKey('clubs.id'))
    squad_count = mapped_column(Integer)
    games_count = mapped_column(Integer)
    wins = mapped_column(Integer)
    draws = mapped_column(Integer)
    losses = mapped_column(Integer)
    goals_scored = mapped_column(Integer)
    goals_received = mapped_column(Integer)
    goal_differences = mapped_column(Integer)
    points = mapped_column(Integer)
    avg_age = mapped_column(Float)
    avg_mkv = mapped_column(Float)
    total_mkv = mapped_column(Float)


class Player(Base):
    __tablename__ = "players"
    id = mapped_column(Integer, primary_key=True)
    player_name = mapped_column(String(32))
    date_of_birth = mapped_column(String(32))
    height = mapped_column(Float, nullable=True)
    foot = mapped_column(String(8))


class Squad(Base):
    __tablename__ = "squad"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id = mapped_column(Integer, ForeignKey('seasons.id'))
    club_id = mapped_column(Integer, ForeignKey('clubs.id'))
    player_id = mapped_column(Integer, ForeignKey('players.id'))
    position = mapped_column(String(32))
    age = mapped_column(Float)
    mk_value = mapped_column(Float)
    agent = mapped_column(String(128))


class GKPerformance(Base):
    __tablename__ = "gk_stats"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id = mapped_column(Integer, ForeignKey('seasons.id'))
    player_id = mapped_column(Integer, ForeignKey('players.id'))
    total_games = mapped_column(Integer)
    games_played = mapped_column(Integer)
    ppg = mapped_column(Float)
    yellow_cards = mapped_column(Integer)
    second_yellow_cards = mapped_column(Integer)
    red_cards = mapped_column(Integer)
    goals_conceded = mapped_column(Integer)
    clean_sheets = mapped_column(Integer)


class OPPerformance(Base):
    __tablename__ = "outfield_stats"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id = mapped_column(Integer, ForeignKey('seasons.id'))
    player_id = mapped_column(Integer, ForeignKey('players.id'))
    total_games = mapped_column(Integer)
    games_played = mapped_column(Integer)
    goals = mapped_column(Integer)
    assists = mapped_column(Integer)
    ppg = mapped_column(Float)
    yellow_cards = mapped_column(Integer)
    second_yellow_cards = mapped_column(Integer)
    red_cards = mapped_column(Integer)


class Transfer(Base):
    __tablename__ = "transfers"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id = mapped_column(Integer, ForeignKey('players.id'))
    season_id = mapped_column(Integer, ForeignKey('seasons.id'))
    from_club = mapped_column(Integer, ForeignKey('clubs.id'))
    to_club = mapped_column(Integer, ForeignKey('clubs.id'))
    mk_value = mapped_column(Float)
    fee = mapped_column(String(32))


class ChampLeague(Base):
    __tablename__ = "champions_league"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id = mapped_column(Integer, ForeignKey('seasons.id'))
    club_id = mapped_column(Integer, ForeignKey('clubs.id'))

Base.metadata.create_all(engine)



# Creating a session in order to insert data to the database tables:

session = Session(engine)

# Inserting data to database tables:

for se in seasons:

    seasons_obj = Season(
        id = int(se['season_id']),
        season_name = se['season_name']
    )
    session.add(seasons_obj)
session.commit()

for cnt in countries:

    country_obj = Country(
        id = int(cnt['country_id']),
        country_name = cnt['country_name']
    )
    session.add(country_obj)
session.commit()

for lg in unique_leagues:

    leagues_obj = League(
        id = lg['league_id'],
        league_name = lg['name'],
        country_id = int(lg['country_id'])
    )
    session.add(leagues_obj)
session.commit()

for clb in clubs:
    try:
        clubs_obj = Club(
            id = clb['club_id'],
            league_id = clb['league_id'],
            club_name = clb['name']
        )
        session.add(clubs_obj)
    except:
        print('error')

session.commit()

for i, clb in club_se.iterrows():

    clubs_se_obj = ClubSeasonal(
        season_id = clb['season_id'],
        club_id = clb['club_id'],
        squad_count = clb['squad_number'],
        games_count = clb['num_games'],
        wins = clb['wins'],
        draws = clb['draws'],
        losses = clb['losses'],
        goals_scored = clb['goals_scored'],
        goals_received = clb['goals_conceded'],
        goal_differences = clb['goal_differences'],
        points = clb['points'],
        avg_age = clb['avg_age'],
        avg_mkv = clb['avg_mkv'],
        total_mkv = clb['total_mkv']
    )
    session.add(clubs_se_obj)
session.commit()

for lg in leagues:

    lg_se_obj = LeagueSeasonal(
        season_id = lg['season_id'],
        league_id = lg['league_id'],
        champion_id = lg['champion_id']
    )
    session.add(lg_se_obj)
session.commit()

for i,player in unique_players_df.iterrows():
    player_obj = Player(
        id = player['player_id'],
        player_name = player['Name'],
        date_of_birth = player['Date_of_birth'],
        height = palyer_height_clean(player['Height']),
        foot = player['Foot']
    )
    session.add(player_obj)
session.commit()

for i,player in players_df.iterrows():
    player_obj = Squad(
        player_id = player['player_id'],
        season_id = player['Season_year'],
        club_id = player['Current_club_ID'],
        position = player['Main_position'],
        age = age_clean(player['Age']),
        mk_value = mkv_clean(player['Market_Value']),
        agent = player['Ajent']
    )
    session.add(player_obj)
session.commit()

for gk in gk_stat:
    player_obj = GKPerformance(
        season_id = gk['season_id'],
        player_id = gk['player_id'],
        total_games = performance_clean(gk['total_games']),
        games_played = performance_clean(gk['games_played']),
        ppg = performance_clean(gk['ppg']),
        yellow_cards = performance_clean(gk['yellow_cards']),
        second_yellow_cards = performance_clean(gk['second_yellow_cards']),
        red_cards = performance_clean(gk['red_cards']),
        goals_conceded = performance_clean(gk['goals_conceded']),
        clean_sheets = performance_clean(gk['clean_sheets'])
    )
    session.add(player_obj)
session.commit()

for out in out_stat:
    player_obj = OPPerformance(
        season_id = out['season_id'],
        player_id = out['player_id'],
        total_games = performance_clean(out['total_games']),
        games_played = performance_clean(out['games_played']),
        goals = performance_clean(out['goals']),
        assists = performance_clean(out['assists']),
        ppg = performance_clean(out['ppg']),
        yellow_cards = performance_clean(out['yellow_cards']),
        second_yellow_cards = performance_clean(out['second_yellow_cards']),
        red_cards = performance_clean(out['red_cards'])
    )
    session.add(player_obj)
session.commit()

for trans in transfers:
    transfer_obj = Transfer(
        player_id = trans['player_id'],
        season_id = season_cleaner(str(trans['season'])),
        from_club = trans['from_id'],
        to_club = trans['to_id'],
        mk_value = mkv_cleaner(trans['market_value']),
        fee = trans['fee']
    )
    session.add(transfer_obj)
session.commit()

for champ in chamions_league:
    champ_obj = ChampLeague(
        season_id = champ['season'],
        club_id = champ['club_id']
        )
    session.add(champ_obj)
session.commit()

print('finished successfully.')