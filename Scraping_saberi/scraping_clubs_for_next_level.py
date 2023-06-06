import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
import json

with open("D:\project\Transfermarket-project\Scraping\SCL.json", "r") as file:
    imported_data = json.load(file)

leagues = imported_data[2]
clubs_for_nextlayer = []

for i in tqdm(range(len(leagues)), desc="Loading..."):
    try:
        url = leagues[i]['LINK']
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})
        soup = BeautifulSoup(page.content, 'html.parser')
        for team in soup.find(id="yw1_c0").find_next('tbody').find_all('tr'):

            clubs = {}
            clubs['name'] = team.find(class_="hauptlink no-border-links").find('a').text
            clubs['club_id'] = team.find(class_="hauptlink no-border-links").find('a').get('href').split('verein/')[1].split('/saison_id')[0]
            clubs['LINK'] = 'https://www.transfermarkt.com' + team.find(class_="hauptlink no-border-links").find('a').get('href')

            clubs_for_nextlayer.append(clubs)
    except:
        print('Something went wrong! request was sent to: {} -- with respose code = {}'.format(url, page.status_code))



with open("clubs_for_nextlayer.json", "w") as file:
    json.dump(clubs_for_nextlayer, file)

