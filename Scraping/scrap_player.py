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
    print('https://www.transfermarkt.com/' + n[i].get('href'))


#name player
n = soup_link.select('.nowrap a')
for i in range (0,len(n),2):
    print(n[i].text)


#primry key for each player
n = soup_link.select('.nowrap a')
for i in range (0,len(n),2):
    number1 = re.search(r'\d+$', n[i].get('href')).group()
    print(number1)