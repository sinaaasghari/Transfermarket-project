#This file is for the crawling part of the Project

import requests
from http.client import responses
from bs4 import BeautifulSoup
import json

links = []
k = 1
header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    'Accept-Language': 'en'
}
page = requests.get("https://www.transfermarkt.com", headers = header)
soup = BeautifulSoup(page.content, 'html.parser')

saison_id = {'21/22':2021, '20/21':2020, '19/20':2019, '18/19':2018, '17/18':2017, '16/17':2016, '15/16':2015}
leagues = {
"E_url":"https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1",
"G_url":"https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1",
"I_url":"https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1",
"F_url":"https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1",
"S_url":"https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1"
}

for key1, value1 in leagues.items():
    for key2, value2 in saison_id.items():
        url1 = value1 + "/plus/?saison_id=" + str(value2)
        page1 = requests.get(url1, headers = header)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        headlines1 = soup1.select('#yw1 .no-border-links a')
        for link1 in headlines1:
            if link1['href'] != '#':
                url2 = "https://www.transfermarkt.com" + link1['href']
            else:
                continue
            page2 = requests.get(url2, headers = header)
            soup2 = BeautifulSoup(page2.content, 'html.parser')
            headlines2 = soup2.select('.nowrap a')
            for link2 in headlines2:
                if k == link2['href']:
                    continue
                else:
                    url3 = "https://www.transfermarkt.com" + link2['href'].replace('profil', 'transfers')
                    links.append(url3)
                k = link2['href']
            


links1 = list(set(links))
with open("players_links.json", "w") as f1:
    json.dump(links1, f1)