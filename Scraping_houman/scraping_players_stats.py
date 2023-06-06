import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
import json
import pandas as pd

leagues = [{'country_id': 'GB1', 'country_name': 'England'},
            {'country_id': 'L1', 'country_name': 'Germany'},
            {'country_id': 'IT1', 'country_name': 'Italy'},
            {'country_id': 'FR1', 'country_name': 'France'},
            {'country_id': 'ES1', 'country_name': 'Spain'}]

with open("Data_of_player.json", 'r') as file:
    file_contents = file.read()
    import_data = json.loads(file_contents)

import_data = pd.DataFrame(import_data)

goalkeepers = []
outfield_players = []

for i in range(len(import_data)):
    player_name = import_data['Name'][i]
    player_id = import_data['player_id'][i]
    season_id = import_data['Season_year'][i]
    url = f"https://www.transfermarkt.com/{player_name}/leistungsdatendetails/spieler/{player_id}/plus/1?saison={season_id}&verein=&liga=1&wettbewerb=&pos=&trainer_id="
    print(url)
    try:
        page = requests.get(url,headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"})
        soup = BeautifulSoup(page.content, 'html.parser')
        smt = soup.select("tfoot .zentriert")
    except:
        print("failed to gather data")
        continue
    if import_data['Main_position'][i] == 'Goalkeeper':
        try:
            goalkeeper = {}
            goalkeeper['season_id'] = season_id
            goalkeeper['player_id'] = player_id
            goalkeeper['total_games'] = smt[0].text
            goalkeeper['games_played'] = smt[1].text
            goalkeeper['ppg'] = smt[2].text
            goalkeeper['yellow_cards'] = smt[7].text
            goalkeeper['second_yellow_cards'] = smt[8].text
            goalkeeper['red_cards'] = smt[9].text
            goalkeeper['goals_conceded'] = smt[10].text
            goalkeeper['clean_sheets'] = smt[11].text
            goalkeepers.append(goalkeeper)
        except:
            print("failed")
            continue
    else:
        outfield_player = {}
        try:
            outfield_player['season_id'] = season_id
            outfield_player['player_id'] = player_id
            outfield_player['total_games'] = smt[0].text
            outfield_player['games_played'] = smt[1].text
            outfield_player['ppg'] = smt[2].text
            outfield_player['goals'] = smt[3].text
            outfield_player['assists'] = smt[4].text
            outfield_player['yellow_cards'] = smt[7].text
            outfield_player['second_yellow_cards'] = smt[8].text
            outfield_player['red_cards'] = smt[9].text
            outfield_players.append(outfield_player)
        except:
            print("failed")
            continue
    print(i ,"/", len(import_data))


with open("gk_stats.json", "w") as outfile:
    json.dump(goalkeepers, outfile)

with open("outfield_stats.json", "w") as outfile:
    json.dump(outfield_players, outfile)
