import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
import json


with open("SCL.json", "r") as file:
    import_data = json.load(file)

team_performances = []
for league in import_data[2]:
    
    team_url = league['LINK'].replace('.com/', '.de/').replace('/startseite/', '/tabelle/')
    team_page = requests.get(team_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})
    team_soup = BeautifulSoup(team_page.content, 'html.parser')
    team_page.status_code
    season = team_url[-4:]
    for row in team_soup.find(id="yw1").find('tbody').find_all('tr'):
        columns = row.find_all('td')
        club_name = columns[2].find('a').text
        club_id = columns[2].find('a').get('href').split('verein/')[1].split('/saison_id')[0]
        num_games = columns[3].text
        wins = columns[4].text
        draws = columns[5].text
        losses = columns[6].text
        goals_scored = columns[7].text.split(':')[0]
        goals_conceded = columns[7].text.split(':')[1]
        goal_differences = columns[8].text
        point = columns[9].text
        team_performances.append({'season_id': season, 'club_name': club_name, 'club_id': club_id, 'num_games': num_games, 'wins': wins, 'draws': draws, 'losses': losses, 'goals_scored': goals_scored, 'goals_conceded': goals_conceded, 'goal_differences': goal_differences, 'points': point})


df_perform = pd.DataFrame(team_performances)
with open("Clubs_and_ClubsBySeasons.json", "r") as file:
    clubs = json.load(file)

df_seasonal = pd.DataFrame(clubs[1])
merged_df = pd.merge(df_perform, df_seasonal, on=['season_id', 'club_id'])
merged_df.to_csv("seasonal_clubs_with_performances.csv", index=False)