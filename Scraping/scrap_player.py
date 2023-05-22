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

#change conditon of rule
Players = []
for i in range(100):
    response_link = requests.get("link_of_json_arsalan", headers=headers)
    response_link.content.decode()
    soup_link = BeautifulSoup(response_link.content, 'html.parser')
    n = soup_link.select('.nowrap a')
    for i in range (0,len(n),2):
        response_player = requests.get('https://www.transfermarkt.com' + n[i].get('href'), headers=headers)
        response_player.content.decode()
        soup_player = BeautifulSoup(response_player.content, 'html.parser')
        Player = {}
        try:
            number = re.search(r'\d+$', n[i].get('href')).group()
            Player['player_id'] = number
        except:
            Player['player_id'] = np.nan
        
        try:
            Player['Name'] = n[i].text
        except:
            Player['Name'] = np.nan
        
        try:
            Player['Main_position'] = soup_player.select('.detail-position__position')[0].text
        except:
            Player['Main_position'] = np.nan
        
        try:
            nt = soup_player.select('.tm-player-market-value-development__current-value')[0].text
            nt = nt.strip()
            nt = nt.replace('€', '')
            if nt[-1:] == 'm':
                vlaue = float(nt[:-1]) * 1000000
            else:
                vlaue = float(nt[:-1]) * 1000

            Player['Market_Value'] = vlaue
        except:
            Player['Market_Value'] = np.nan



            
            text = soup_player.select('.info-table--right-space')[0].text
            # Extracting Date of birth
            dob_pattern = r"Date of birth:\n(.*?)\n"
            dob_match = re.search(dob_pattern, text)
            if dob_match:
                date_of_birth = dob_match.group(1)
            else:
                date_of_birth = np.nan

            # Extracting Age
            age_pattern = r"Age:\n(.*?)\n"
            age_match = re.search(age_pattern, text)
            if age_match:
                age = int(age_match.group(1))
            else:
                age = np.nan

            # Extracting Foot
            foot_pattern = r"Foot:\n(.*?)\n"
            foot_match = re.search(foot_pattern, text)
            if foot_match:
                foot = foot_match.group(1)
            else:
                foot = np.nan

            # Extracting Player agent
            agent_pattern = r"Player agent:\n\n(.*?)\n\n"
            agent_match = re.search(agent_pattern, text)
            if agent_match:
                player_agent = agent_match.group(1)
            else:
                player_agent = np.nan

            # Extracting Height
            height_pattern = r"Height:\n(.*?)\xa0"
            height_match = re.search(height_pattern, text)
            if height_match:
                height = height_match.group(1)
            else:
                height = np.nan

            Player['Date_of_birth'] = date_of_birth
            Player['Age'] = age
            Player['Height'] = height
            Player['Foot'] = foot
            Player['Ajent'] = player_agent
            Player['Current_club_ID']

            Players.append(Player)
            

