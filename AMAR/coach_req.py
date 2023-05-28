import json
import re
import pandas as pd
import time
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


#-----------------------------------------------------GK_part-------------------------------------------------------------------------
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



#'apprance'0.4, 'goals_conceded'-0.4,'clean_sheets'0.2,'ppg'0.15, 'yellow_cards'-0.05, 'second_yellow_cards'-0.05, 'red_cards'-0.05
#set_metric
df1["score"] = df1["apprance"] * 0.4 + df1["goals_conceded"] * -0.4 + df1["clean_sheets"] * 0.2 + df1["ppg"] * 0.15 + df1["yellow_cards"] * -0.05 + df1["second_yellow_cards"] * -0.05 + df1["red_cards"] * -0.05

#sort_by score
df1 = df1.sort_values("score" , ascending=False)
df_gk = df1["player_name"].unique()
df_gk_final = pd.DataFrame(df_gk, columns=["name"])

#Keeping the first thirty percent of the data
df_gk_30 = df_gk_final.head(293)


#-----------------------------------------------------player_part-------------------------------------------------------------------------
#clear the data like last part
df = pd.read_csv("Player.csv")
df.drop(['id','id.1','id.2', 'season_id.1', 'club_id', 'player_id.1',
       'age'], axis=1, inplace=True)
df1 = df.copy()


df1["apprance"] = df1["games_played"] / df1["total_games"] 
df1.drop(["total_games","games_played"], axis=1, inplace=True)


df1.fillna(0, inplace=True)

columns_to_scale = ['apprance', 'ppg',
       'yellow_cards', 'second_yellow_cards', 'red_cards', 'goals',
       'assists']

#we wanna just 2021 data
values_to_drop= [2015, 2016, 2017, 2018, 2019, 2020]

df1 = df1[~df1['season_id'].isin(values_to_drop)]


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 100))
df1[columns_to_scale] = scaler.fit_transform(df1[columns_to_scale])

df2 = df1.copy()
df2.drop(['season_id', 'player_id','player_name', 'date_of_birth', 'height', 'foot',
       'position', 'mk_value', 'agent'], axis=1 ,inplace=True)

corr_matrix = df2.corr()


fig1, ax1 = plt.subplots(figsize=(15, 10))
fig1.set_facecolor('lightgray')
sns.heatmap(corr_matrix, cmap='viridis', annot=True,ax=ax1)
ax1.set_title('correlation heatmap')


#-----------------------------------------------------player_attakcer_part-------------------------------------------------------------------------
values_to_drop__hamle = ['Attacking Midfield','Central Midfield', 'Left Midfield', 'Right-Back',
       'Defensive Midfield', 'Left-Back', 'Right Midfield', 'Centre-Back',
       0]

# drop that postion ther are not in attack pos
df_hamle=df1.copy()
df_hamle = df_hamle[~df_hamle['position'].isin(values_to_drop__hamle)]

#calculate score for each player
df_hamle["score"] = df_hamle["apprance"] * 0.3 + df_hamle["goals"] * 0.3 + df_hamle["assists"] * 0.15 + df_hamle["ppg"] * 0.1 + df_hamle["yellow_cards"] * -0.05 + df_hamle["second_yellow_cards"] * -0.05 + df_hamle["red_cards"] * -0.05  

#save the name of player that have high score
df_hamle = df_hamle.sort_values("score" , ascending=False)
df_hamle_temp = df_hamle["player_name"].unique()

df_hamle_final= pd.DataFrame(df_hamle_temp, columns=["name"])

#-----------------------------------------------------player_midfiedl_part-------------------------------------------------------------------------
#like attaker part
values_to_drop_hafbak = ['Centre-Forward', 'Right Winger', 'Second Striker', 'Left Winger',
       'Right-Back', 'Defensive Midfield',
       'Left-Back', 'Centre-Back', 0]

df_hafback=df1.copy()
df_hafback = df_hafback[~df_hafback['position'].isin(values_to_drop_hafbak)]

df_hafback["score"] = df_hafback["apprance"] * 0.3 + df_hafback["goals"] * 0.15 + df_hafback["assists"] * 0.3 + df_hafback["ppg"] * 0.1 + df_hafback["yellow_cards"] * -0.05 + df_hafback["second_yellow_cards"] * -0.05 + df_hafback["red_cards"] * -0.05
df_hafback = df_hafback.sort_values("score" , ascending=False)
df_hafback_temp = df_hafback["player_name"].unique()
df_hafback_final= pd.DataFrame(df_hafback_temp, columns=["name"])
#-----------------------------------------------------player_defence_part-------------------------------------------------------------------------
#like attaker part

values_to_drop_defa = ['Centre-Forward', 'Right Winger', 'Second Striker', 'Left Winger',
       'Attacking Midfield', 'Central Midfield', 'Left Midfield',
       'Right Midfield', 0]


df_defa=df1.copy()
df_defa = df_defa[~df_defa['position'].isin(values_to_drop_defa)]

df_defa["score"] = df_defa["apprance"] * 0.5 + df_defa["ppg"] * 0.4 + df_defa["yellow_cards"] * -0.3 + df_defa["second_yellow_cards"] * -0.5 + df_defa["red_cards"] * -0.5

df_defa = df_defa.sort_values("score" , ascending=False)
df_defa_temp = df_defa["player_name"].unique()

df_defa_final = pd.DataFrame(df_defa_temp, columns=["name"])
#-----------------------------------------------------30% of player-------------------------------------------------------------------------
df_hamle_final.shape #264
df_hamle_30 = df_hamle_final.head(264)

df_defa_final.shape #402
df_defa_30 = df_defa_final.head(402)

df_hafback_final.shape #202
df_hafback_30 = df_hafback_final.head(202)