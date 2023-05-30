import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import json
import re

with open('transfer_stats.json', 'r') as f1:
    transfers = json.load(f1)



df = pd.DataFrame(transfers)

transfers_main = []
for i in transfers:
    match = re.search('\d+', i['fee'])
    if match and i['season'] >= 2017 and i['season'] <= 2021 and i['market_value'] != 'None':
        i['fee'] = int(match.group(0))
        i['market_value'] = int(float(i['market_value']))
        transfers_main.append(i)

df1 = pd.DataFrame(transfers_main)

data = df1.groupby('season').mean()[['market_value', 'fee']].reset_index()
data['market_value'] = data['market_value'].astype(int)
data['fee'] = data['fee'].astype(int)
def millions_formatter(x, pos):
    return '{:.0f}M'.format(x/1000000)



fig, ax = plt.subplots(figsize=(9,7.5))
h1 = ax.bar(data['season'], data['market_value'], color= 'purple', alpha = 1, width=0.45, label='market_value')
h2 = ax.bar(data['season'], data['fee'], color= 'black', alpha= 0.5, width=0.5, label='fee')

ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

plt.grid(axis='y')
ax.legend()
plt.show()


