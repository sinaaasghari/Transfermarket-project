import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import ttest_ind

with open('seasonal_clubs_with_performances.csv', 'r') as f:
    all_clubs = pd.read_csv(f)

with open('transfermarkt_squad_attack.csv', 'r') as f:
    players = pd.read_csv(f)

with open('transfermarkt_squad_defender.csv', 'r') as f:
    defenders = pd.read_csv(f)
    
with open('transfermarkt_outfield_stats.csv', 'r') as f:
    players_2021 = pd.read_csv(f)
players_2021['appearances'] = players_2021['games_played'] / players_2021['total_games']

#conver all - to 0
players_2021 = players_2021.fillna(0)

# players_2021 = players_2021.astype({'total_games': 'float64', 'ppg': 'float64', 
#                                           'yellow_cards': 'float64', 'second_yellow_cards': 'float64',
#                                           'red_cards': 'float64', 'goals': 'float64', 'assists': 'float64'})
clubs_2021 = all_clubs.loc[all_clubs['season_id'] == 2021]
df1 = players_2021.copy()
columns_to_scale = ['appearances','total_games', 'ppg',
       'yellow_cards', 'second_yellow_cards', 'red_cards', 'goals',
       'assists']

scaler = MinMaxScaler(feature_range=(0, 100))
df1[columns_to_scale] = scaler.fit_transform(df1[columns_to_scale])


df2 = df1.copy()
df2 = df1.loc[df1['player_id'].isin(players['player_id'])]

df_hamle = df1.copy()
df_hamle["score"] = df_hamle["appearances"] * 0.3 + df_hamle["goals"] * 0.3 + df_hamle["assists"] * 0.15 + df_hamle["ppg"] * 0.1 + df_hamle["yellow_cards"] * -0.05 + df_hamle["second_yellow_cards"] * -0.05 + df_hamle["red_cards"] * -0.05
df_hamle = df_hamle.merge(players[['player_id', 'club_id']], on='player_id', how='left')
df_hamle = df_hamle.sort_values("score" , ascending=False)


df_defa = df1.loc[df1['player_id'].isin(defenders['player_id'])]
df_defa["score"] = df_defa["appearances"] * 0.5 + df_defa["ppg"] * 0.4 + df_defa["yellow_cards"] * -0.3 + df_defa["second_yellow_cards"] * -0.5 + df_defa["red_cards"] * -0.5

# for each player get club id from defenders
df_defa = df_defa.merge(defenders[['player_id', 'club_id']], on='player_id', how='left')
df_defa = df_defa.sort_values("score" , ascending=False)

clubs = pd.DataFrame()
#for every club id in df_defa get the sum of the scores
clubs['defence_score'] = df_defa.groupby('club_id')['score'].sum()
clubs['attack_score'] = df_hamle.groupby('club_id')['score'].sum()
clubs['diffrence'] = clubs['defence_score'] - clubs['attack_score']

#get the most defensive and least offensive clubs
clubs = clubs.sort_values("diffrence" , ascending=False)

# clubs : 
# 1. chelsea Fc
# 2. west ham united