import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import ttest_ind

scaler = MinMaxScaler(feature_range=(0, 100))

with open('Champions_league.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)

cl_clubs = df['club_id'].tolist()
cl_clubs = [int(cl_clubs[x]) for x in range(len(cl_clubs))]

with open('seasonal_clubs_with_performances.csv', 'r') as f:
    data = pd.read_csv(f)
df = pd.DataFrame(data)

clubs_2021 = df.loc[df['season_id'] == 2021]

cl_clubs_league = clubs_2021.loc[clubs_2021['club_id'].isin(cl_clubs)]
#print(cl_clubs_league)

not_cl_clubs_league = clubs_2021.loc[~clubs_2021['club_id'].isin(cl_clubs)]
#print(not_cl_clubs_league)

print(cl_clubs_league['points'].mean())
print(not_cl_clubs_league['points'].mean())
print("wins:")

print(cl_clubs_league['wins'].mean())
print(not_cl_clubs_league['wins'].mean())
print("losses:")

print(cl_clubs_league['losses'].mean())
print(not_cl_clubs_league['losses'].mean())

print("goal_diffrence")
print(cl_clubs_league['goal_differences'].mean())
print(not_cl_clubs_league['goal_differences'].mean())
t_statistic, p_value = ttest_ind(cl_clubs_league['points'], not_cl_clubs_league['points'])

print("t-statistic:", t_statistic)
print("p-value:", p_value)