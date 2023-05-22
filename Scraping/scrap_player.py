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

