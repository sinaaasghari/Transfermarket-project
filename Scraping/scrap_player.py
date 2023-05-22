import requests
import json
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import re
import numpy as np

headers = {
    'Accept-Language': 'en-US',
    "User-Agent": "Chrome/112.0.5615.138"
}

#get links in feature
response_link = requests.get('https://www.transfermarkt.com/chelsea-fc/startseite/verein/631?saison_id=2020', headers=headers)
response_link.content.decode()
soup_link = BeautifulSoup(response_link.content, 'html.parser')

#link each player
n = soup_link.select('.nowrap a')
for i in range (0,len(n),2):
    print('https://www.transfermarkt.com' + n[i].get('href'))


#name player
n = soup_link.select('.nowrap a')
for i in range (0,len(n),2):
    print(n[i].text)


#primry key for each player
n = soup_link.select('.nowrap a')
for i in range (0,len(n),2):
    number = re.search(r'\d+$', n[i].get('href')).group()
    print(number)

#link replce from first part
response_link_player = requests.get('https://www.transfermarkt.com/daryl-janmaat/profil/spieler/60744', headers=headers)
response_link_player.content.decode()
soup_link_player = BeautifulSoup(response_link_player.content, 'html.parser')

#main position
soup_link_player.select('.detail-position__position')[0].text

#market_value
soup_link_player.select('.tm-player-market-value-development__current-value')[0].text

#current_id_club
#give_that_data_from another teammate


text = soup_link_player.select('.info-table--right-space')[0].text

# Extracting Date of birth
dob_pattern = r"Date of birth:\n(.*?)\n"
dob_match = re.search(dob_pattern, text)
if dob_match:
    date_of_birth = dob_match.group(1)
else:
    date_of_birth = None

# Extracting Age
age_pattern = r"Age:\n(.*?)\n"
age_match = re.search(age_pattern, text)
if age_match:
    age = age_match.group(1)
else:
    age = None

# Extracting Foot
foot_pattern = r"Foot:\n(.*?)\n"
foot_match = re.search(foot_pattern, text)
if foot_match:
    foot = foot_match.group(1)
else:
    foot = None

# Extracting Player agent
agent_pattern = r"Player agent:\n\n(.*?)\n\n"
agent_match = re.search(agent_pattern, text)
if agent_match:
    player_agent = agent_match.group(1)
else:
    player_agent = None

# Extracting Height
height_pattern = r"Height:\n(.*?)\xa0"
height_match = re.search(height_pattern, text)
if height_match:
    height = height_match.group(1)
else:
    height = None

print("Date of birth:", date_of_birth)
print("Age:", age)
print("Foot:", foot)
print("Player agent:", player_agent)
print("Height:", height)

