import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
import json

#seasons table content
seasons = [{'season_id': '2015', 'season_name': '15/16'},
           {'season_id': '2016', 'season_name': '16/17'},
           {'season_id': '2017', 'season_name': '17/18'},
           {'season_id': '2018', 'season_name': '18/19'},
           {'season_id': '2019', 'season_name': '19/20'},
           {'season_id': '2020', 'season_name': '20/21'},
           {'season_id': '2021', 'season_name': '21/22'}]

#countries table content
countries = [{'country_id': '189', 'country_name': 'England'},
             {'country_id': '40', 'country_name': 'Germany'},
             {'country_id': '75', 'country_name': 'Italy'},
             {'country_id': '50', 'country_name': 'France'},
             {'country_id': '157', 'country_name': 'Spain'}]

#scraping leagues data
leagues = []
for i in tqdm(range(len(countries)), desc="Loading..."):
    for n in range(len(seasons)):
        try:
            league = {}

            lg_url = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/{}/plus/0?saison_id={}'.format(countries[i]['country_id'], seasons[n]['season_id'])
            lg_page = requests.get(lg_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})

            lg_soup = BeautifulSoup(lg_page.content, 'html.parser')
            target_tag = lg_soup.find(lambda tag: tag.name == 'td' and 'First Tier' in tag.get_text()).find_next('tr')
            lg = target_tag.find(class_="hauptlink").find('a')
            champ = target_tag.find(class_="zentriert").find('a')

            league['league_id'] = lg.get('href').split('wettbewerb/')[1].split('/saison_id')[0]
            league['name'] = lg.text
            league['country_id'] = countries[i]['country_id']
            league['season_id'] = seasons[n]['season_id']
            league['champion_id'] = champ.get('href').split('verein/')[1].split('/saison_id')[0]
            league['LINK']  =  'https://www.transfermarkt.com{}'.format(lg.get('href'))

            leagues.append(league)

        except:
            print('request was sent to: {} -- with respose code = {}'.format(lg_url, lg_page.status_code))
            print('something went wrong with this item')
        
        
        # Sleep for a random time to avoid being blocked
        time_milliseconds = randint(200, 1000)
        time_sec = 0.001 * time_milliseconds
        sleep(time_sec)

scraped_data = [seasons, countries, leagues]

with open("SCL.json", "w") as file:
    json.dump(scraped_data, file)