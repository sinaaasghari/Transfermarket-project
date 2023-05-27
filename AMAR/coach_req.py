import json
import re
import pandas as pd
import time
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

#read file
df = pd.read_csv('GK.csv')
df1 = df.copy()
df1.drop(['id','id.1','id.2', 'season_id.1', 'club_id', 'player_id.1',
       'age'], axis=1, inplace=True)


#set_apprance
df1["apprance"] = df1["games_played"] / df1["total_games"] 
df1.drop(["total_games","games_played"], axis=1, inplace=True)

#fill null value
df1.fillna(0, inplace=True)

columns_to_scale = ['apprance', 'ppg',
       'yellow_cards', 'second_yellow_cards', 'red_cards', 'goals_conceded',
       'clean_sheets']


#change scale
scaler = MinMaxScaler(feature_range=(0, 100))
df1[columns_to_scale] = scaler.fit_transform(df1[columns_to_scale])


df2 = df1.copy()
df2.drop(['season_id', 'player_id','player_name', 'date_of_birth', 'height', 'foot',
       'position', 'mk_value', 'agent'], axis=1 ,inplace=True)


#corrlation_matrix
corr_matrix = df2.corr()
fig1, ax1 = plt.subplots(figsize=(15, 10))
fig1.set_facecolor('lightgray')
sns.heatmap(corr_matrix, cmap='viridis', annot=True,ax=ax1)
ax1.set_title('correlation heatmap')



#'apprance'0.3, 'goals_conceded'0.25,'clean_sheets'0.15,'ppg'0.1, 'yellow_cards'0.1, 'second_yellow_cards'0.05, 'red_cards'0.05
#set_metric
df1["score"] = df1["apprance"] * 0.3 + df1["goals_conceded"] * -0.2 + df1["clean_sheets"] * 0.2 + df1["ppg"] * 0.15 + df1["yellow_cards"] * -0.05 + df1["second_yellow_cards"] * -0.05 + df1["red_cards"] * 0.05