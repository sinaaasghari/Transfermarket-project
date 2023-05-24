import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
import json


seasons = [{'season_id': '2015', 'season_name': '15/16'},
           {'season_id': '2016', 'season_name': '16/17'},
           {'season_id': '2017', 'season_name': '17/18'},
           {'season_id': '2018', 'season_name': '18/19'},
           {'season_id': '2019', 'season_name': '19/20'},
           {'season_id': '2020', 'season_name': '20/21'},
           {'season_id': '2021', 'season_name': '21/22'}]

leagues = [{'country_id': 'GB1', 'country_name': 'England'},
            {'country_id': 'L1', 'country_name': 'Germany'},
            {'country_id': 'IT1', 'country_name': 'Italy'},
            {'country_id': 'FR1', 'country_name': 'France'},
            {'country_id': 'ES1', 'country_name': 'Spain'}]

# url = "https://www.transfermarkt.com/ederson/leistungsdatendetails/spieler/238223/saison/2022/verein/0/liga/0/wettbewerb/GB1/pos/0/trainer_id/0/plus/1"
# page = requests.get(url,headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})

# soup = BeautifulSoup(page.content, 'html.parser')

# smt = soup.select("tfoot .zentriert")
# # smt[0] = Total Games
# # smt[1] = Games played
# # smt[2] = ppg
# # smt[7] = yellow cards
# # smt[8] = second yellow cards
# # smt[9] = red cards
# # smt[10] = Goals conceded
# # smt[11] = Clean sheets
# print(smt[0].text)
# print(smt[1].text)


# url = "https://www.transfermarkt.com/joao-cancelo/leistungsdatendetails/spieler/182712/saison/2022/verein/0/liga/0/wettbewerb/L1/pos/0/trainer_id/0/plus/1"
# page = requests.get(url,headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})
# soup = BeautifulSoup(page.content, 'html.parser')
# info = soup.select('.data-header__items .data-header__content')
# check_array = []
# for i in range(len(info)):
#     check_array.append(info[i].text.strip())
# if 'Right-Back' in check_array:
#     print('Goalkeeper')

with open("Transfermarket-project\Scraping\players_links.json", 'r') as file:
    file_contents = file.read()
    import_data = json.loads(file_contents)

import_data = list(set(import_data))

goalkeepers = []
outfield_players = []

for i in import_data:
    link = i.split('/')
    # -1 = player_id
    # -4 = player_name
    player_name = link[-4]
    player_id = link[-1]
    for league in leagues:
        for season in seasons:
            url = f"https://www.transfermarkt.com/{player_name}/leistungsdatendetails/spieler/{player_id}/saison/{season['season_id']}/verein/0/liga/0/wettbewerb/{league['country_id']}/pos/0/trainer_id/0/plus/1"
            print(url)
            page = requests.get(url,headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9'})
            soup = BeautifulSoup(page.content, 'html.parser')
            info = soup.select('.data-header__items .data-header__content')
            check_array = []
            try:
                for i in range(len(info)):
                    check_array.append(info[i].text.strip())
            except:
                continue


            # Goalkeepers
            if ' Goalkeeper' in check_array:
                goalkeeper = {}
                smt = soup.select("tfoot .zentriert")
                # smt[0] = Total Games
                # smt[1] = Games played
                # smt[2] = ppg
                # smt[7] = yellow cards
                # smt[8] = second yellow cards
                # smt[9] = red cards
                # smt[10] = Goals conceded
                # smt[11] = Clean sheets
                try:    
                    goalkeeper['season_id'] = season['season_id']
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
                    print(smt[0].text)
                    print(smt[1].text)
                    print(smt[2].text)
                    print(smt[7].text)
                    print(smt[8].text)
                    print(smt[9].text)
                    print(smt[10].text)
                    print(smt[11].text)
                except:
                    continue
            
            
            # outfield players
            else:
                outfield_player = {}
                smt = soup.select("tfoot .zentriert")
                # smt[0] = Total Games
                # smt[1] = Games played
                # smt[2] = ppg
                # smt[3] = Goals
                # smt[4] = Assists
                # smt[7] = yellow cards
                # smt[8] = second yellow cards
                # smt[9] = red cards
                try:
                    outfield_player['season_id'] = season['season_id']
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
                    print(smt[0].text)
                    print(smt[1].text)
                    print(smt[2].text)
                    print(smt[7].text)
                    print(smt[8].text)
                    print(smt[9].text)
                    print(smt[10].text)
                    print(smt[11].text)
                except:
                    continue

with open("gk_stats.json", "w") as outfile:
    json.dump(goalkeepers, outfile)

with open("outfield_stats.json", "w") as outfile:
    json.dump(outfield_players, outfile)