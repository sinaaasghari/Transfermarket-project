import json
import re
import pandas as pd
import time
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#read data dropn unuseful parametr
df = pd.read_csv('All_player_with_score.csv')
df.drop(['Unnamed: 0.1', 'Unnamed: 0', 'goals',
       'assists', 'ppg', 'yellow_cards', 'second_yellow_cards', 'red_cards', 'agent', 'apprance', 'goals_conceded',
       'clean_sheets'], axis=1, inplace=True)

#sort to find first season that player played
df.sort_values(['season_id'], ascending=False, inplace=True)
df = df[~df['player_name'].duplicated(keep='last')]

#splite in 2 dataframe old and young
df_old = df[df['age'] >= 30]
df_young = df[df['age'] < 30]
df_young = df_young[df_young['age'] != 0]

#the mean performance old
df_old['score'].mean() #44.22758845958626


#the mean performance young
df_young['score'].mean() #35.45685003646682