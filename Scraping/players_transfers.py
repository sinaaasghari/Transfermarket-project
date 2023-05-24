import requests
from http.client import responses
from bs4 import BeautifulSoup
import json

header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    'Accept-Language': 'en'
}

with open('players__transfers_links.json') as f:
    data = json.load(f)

counter = 1
players = []
saison_id = {'21/22':2021, '20/21':2020, '19/20':2019, '18/19':2018, '17/18':2017, '16/17':2016, '15/16':2015}

for link in data:
    page = requests.get(link, headers = header)
    soup = BeautifulSoup(page.content, 'html.parser')

    finder = []

    for l in soup.select('.tm-player-transfer-history-grid__season, .tm-player-transfer-history-grid__old-club, .tm-player-transfer-history-grid__new-club, .tm-player-transfer-history-grid__fee'):
        if l.text.split() not in ['Fee', 'Season']:
            finder.append(l.text.split())
    del finder[:4]
    ll = {}
    for x in range(0,len(finder)-3,4):
        if len(finder[x]) == 0:
            finder[x] = ['Unknown']
        if len(finder[x+1]) == 0:
            finder[x+1] = ['Unknown']
        if len(finder[x+2]) == 0:
            finder[x+2] = ['Unknown']
        if len(finder[x+3]) == 0:
            finder[x+3] = ['Unknown']
        g0 = str(finder[x][0])
        g1 = str(finder[x+1][0])
        g2 = str(finder[x+2][0])
        g3 = str(finder[x+3][0])
        if g0 not in saison_id.keys():
            continue
        if len(finder[x+1])>1:
            g1 = ''
            for y1 in finder[x+1]:
                g1 += y1 + ' '
        if len(finder[x+2])>1:
            g2 = ''
            for y2 in finder[x+2]:
                g2 += y2 + ' '
        if len(finder[x+3])>1:
            g3 = ''
            for y3 in finder[x+3]:
                g3 += y3 + ' '
        ll = {'player_name':link.split('/')[-4],'player_id':link.split('/')[-1],'Season':g0, 'From_club':g1, 'To_club':g2, 'Fee':g3}
        players.append(ll)
        percent = (counter/len(data))*100
        print(f'{percent}' + '%')
        print(players)
        counter += 1


with open("players_transfers.json", "w") as f1:
    json.dump(players, f1) 