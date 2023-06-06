import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
import json

def mkv_to_int(mkv):
    mkv = mkv.replace('€', '')
    if mkv[-2:] == 'bn':
        vlaue = float(mkv[:-2]) * 1000000000
    elif mkv[-1] == 'm':
        vlaue = float(mkv[:-1]) * 1000000
    elif mkv[-1] == 'k':
        vlaue = float(mkv[:-1]) * 1000
    return vlaue        

with open("D:\project\Transfermarket-project\Scraping\SCL.json", "r") as file:
    imported_data = json.load(file)

leagues = imported_data[2]

clubs = []
clubs_seasonal = []

for i in tqdm(range(len(leagues)), desc="Loading..."):
    url = leagues[i]['LINK']
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})
    soup = BeautifulSoup(page.content, 'html.parser')
    for team in soup.find(id="yw1_c0").find_next('tbody').find_all('tr'):
        

        club = {}
        club_season = {}

        tds = team.find_all('td')

        club_id = tds[1].find('a').get('href').split('verein/')[1].split('/saison_id')[0]
        league_id = leagues[i]['league_id']
        season_id = leagues[i]['season_id']

        if not any(a_team['club_id'] == club_id for a_team in clubs):
            club['club_id'] = club_id
            club['league_id'] = league_id
            club['name'] = tds[1].find('a').text
            clubs.append(club)
        
        club_season['club_id'] = club_id
        club_season['season_id'] = season_id
        club_season['squad_number'] = tds[2].find('a').text
        club_season['avg_age'] = tds[3].text
        club_season['avg_mkv'] = mkv_to_int(tds[5].text)
        club_season['total_mkv'] = mkv_to_int(tds[6].find('a').text)
        club_season['CLUB_IN_SEASON_LINK'] = 'https://www.transfermarkt.com' + tds[1].find('a').get('href')
        club_season['SQUAD_IN_SEASON_LINK'] = 'https://www.transfermarkt.com' + tds[2].find('a').get('href')

        clubs_seasonal.append(club_season)

scraped_data = [clubs, clubs_seasonal]

with open("Clubs_and_ClubsBySeasons.json", "w") as file:
    json.dump(scraped_data, file)