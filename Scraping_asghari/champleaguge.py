import requests
from bs4 import BeautifulSoup
import json


chl_url = 'https://www.transfermarkt.de/uefa-champions-league/teilnehmer/pokalwettbewerb/CL/saison_id/2021'
chl_page = requests.get(chl_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})
chl_soup = BeautifulSoup(chl_page.content, 'html.parser')
chl_page.status_code


champ_league = []
for team in chl_soup.find(id='yw1').find('tbody').find_all(class_="links no-border-links hauptlink"):
    club_id = team.find('a').get('href').split('verein/')[1]
    season = chl_url.split('saison_id/')[1]
    champ_league.append({'club_id': club_id, 'season': season})


with open("Champions_league.json", "w") as file:
    json.dump(champ_league, file)