import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
from PIL import Image
import requests

st.set_page_config(
    page_title="Statistical Analysis",
    page_icon="📊",
)


def player_req():
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
    فرض کنید که یک مهاجم می‌خواهد تیم خود را عوض کند، و به همین دلیل، به دنبال تیم‌هایی می‌گردد که به یک مهاجم نیاز دارند. نیاز یک مهاجم، به این صورت مطرح می‌شود که عملکرد بازیکنان در حمله، بدتر از عملکرد بازیکنان در دفاع باشد. هر تیمی که این ویژگی را داشته باشد، یک گزینه‌ی مناسب به حساب می‌آید. ضمناً، باید تیم‌ها بر اساس نیازشان به مهاجم مرتب شده باشند. یعنی تیمی که اختلاف عملکرد دفاع و حمله‌ش بیشتر باشد، باید در رتبه‌ی بالاتری قرار بگیرد.
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.code("""
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
            """)
    st.dataframe(pd.read_csv('clubs_score_dif.csv'))


def exp_req():
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
    یکی از کارشناسان، می‌خواهد بداند که سایت به چه میزان تخمین درستی از قیمت بازیکنان ارائه می‌دهد. هم‌چنین اخیراً مشکلی در صنعت فوتبال پیش آمده است که بازیکنان با قیمت بسیار بیشتری از ارزش واقعی‌شان معامله می‌شوند. به همین دلیل، در این بخش از شما خواسته شده است که توزیع قیمت تخمین بازیکنان فروخته شده در هر فصل، و قیمت واقعی انتقال‌های هر فصل را با هم مقایسه کنید (از انتقال‌های رایگان صرف نظر کنید).
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.code("""
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


    fig, ax = plt.subplots(figsize=(9,7.5))
    h1 = ax.bar(data['season'], data['market_value'], color= 'purple', alpha = 1, width=0.45, label='market_value')
    h2 = ax.bar(data['season'], data['fee'], color= 'black', alpha= 0.5, width=0.5, label='fee')
    def millions_formatter(x, pos):
        return '{:.0f}M'.format(x/1000000)

    ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    plt.grid(axis='y')
    ax.legend()
    plt.show()
    """)

    st.write("")
    st.write("")
    image = Image.open('statistics_karshenas_plot.png')
    st.image(image,caption="Expert's request")
    st.write("")
    st.write("")


def coach_req():
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
    یک مربی قصد دارد که تیم را برای فصل بعد تقویت کند. به همین دلیل، از شما خواسته است که بازیکنانی را پیدا کنید که عملکرد خیلی خوبی داشته‌اند و در عین حال، قیمت پایینی دارند.
    برای این کار، باید بازیکنانی را پیدا کنید که از لحاظ عملکردی، در ۳۰ درصد برتر قرار می‌گیرند ولی از لحاظ قیمتی، در ۴۰ درصد پایین قرار می‌گیرند.

    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")

    st.code("""
    #-----------------------------------------------------GK_part-------------------------------------------------------------------------
    #read file
    df = pd.read_csv('GK.csv')
    df1 = df.copy()
    df1.drop(['id','id.1','id.2', 'season_id.1', 'club_id', 'player_id.1',
        'age'], axis=1, inplace=True)

    #we wanna just 2021 data
    values_to_drop= [2015, 2016, 2017, 2018, 2019, 2020]

    df1 = df1[~df1['season_id'].isin(values_to_drop)]
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
        """)
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.write("---")

    st.write("")
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">

    نمودار توزیع قیمت بازیکنانی که در قسمت اول بدست آوردید را با کل جامعه‌ی بازیکنان مقایسه کنید.
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('Statistics_morabi1.png')
    st.image(image,caption='Value Comparison')
    st.write("")
    st.write("")
    
    st.write("---")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
    نمودار توزیع عملکرد بازیکنانی که در قسمت اول بدست آوردید را با کل جامعه‌ی بازیکنان مقایسه کنید.
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('Statistics_morabi2.png')
    st.image(image,caption='Performance Comparison')
    st.write("")
    st.write("")

    st.write("---")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
    توزیع پست بازیکنانی که در قسمت اول بدست آوردید را با کل جامعه‌ی بازیکنان مقایسه کنید.
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('Statistics_morabi3.png')
    st.image(image,caption='Position Comparison')
    

    st.write("---")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
    بازیکنانی که عملکرد بدی دارند (داده‌های پرت)
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.dataframe(pd.read_csv('outlier.csv'))
    


def first_hypo():
    st.write("")
    st.write("")

    st.markdown("""
    <div style="text-align: right;">
    فرض یکم: بازیکنان با تجربه (با حداقل ۳۰ سال سن)،‌ در اولین فصل حضورشان در یک تیم جدید، به صورت کلی، عملکرد بهتری نسبت به بازیکنان کم تجربه (با سن کمتر از ۳۰) در اولین فصل‌شان در تیم جدید، دارند.

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.code("""
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
    """)
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">

    :طبق خروجی فرضیه درست است به سه دلیل

    اول: تفاوت سنی: بازیکنان با سن بالاتر معمولاً تجربه‌ی بیشتری در رقابت‌های فوتبالی دارند و احتمالاً مهارت‌های فنی و تصمیم‌گیری بهتری نسبت به بازیکنان جوان‌تر دارند. این تفاوت سنی می‌تواند توجیهی برای عملکرد بهتر بازیکنان با سن بالاتر در اولین فصل حضورشان در تیم جدید باشد.

    دوم: تطابق با سبک بازی تیم: بازیکنان با تجربه ممکن است بهتر بتوانند با سبک بازی و تاکتیک‌های تیم جدید سازگار شوند و سریعاً در بازی تأثیرگذار شوند. این تطابق می‌تواند توجیهی برای عملکرد بهتر بازیکنان با تجربه در اولین فصل حضورشان در تیم جدید باشد.

    سوم: فشار روانی: بازیکنان جوان ممکن است در مقابل فشارهای روانی و انتظارات بزرگتر در تیم جدید دچار مشکل شوند، در حالی که بازیکنان با تجربه ممکن است این فشار را بهتر تحمل کنند و عملکرد بهتری از خود نشان دهند. این فشار روانی می‌تواند توجیهی دیگر برای عملکرد بهتر بازیکنان با تجربه در اولین فصل حضورشان در تیم جدید باشد.
    </div>
    """, unsafe_allow_html=True)


def sec_hypo():
    st.write("")
    st.write("")

    st.markdown("""
    <div style="text-align: right;">
    فرض دوم: عملکرد تیم‌های حاضر در لیگ قهرمانان اروپا، از سایر تیم‌ها، در لیگ بهتر است.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.write("")
    st.write("")

    with st.echo():
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
        st.write("Points:")
        st.write(cl_clubs_league['points'].mean())
        st.write(not_cl_clubs_league['points'].mean())
        
        st.write("wins:")
        st.write(cl_clubs_league['wins'].mean())
        st.write(not_cl_clubs_league['wins'].mean())
        
        st.write("losses:")
        st.write(cl_clubs_league['losses'].mean())
        st.write(not_cl_clubs_league['losses'].mean())

        st.write("goal_diffrence")
        st.write(cl_clubs_league['goal_differences'].mean())
        st.write(not_cl_clubs_league['goal_differences'].mean())
        t_statistic, p_value = ttest_ind(cl_clubs_league['points'], not_cl_clubs_league['points'])

        st.write("t-statistic:", t_statistic)
        st.write("p-value:", p_value)

    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
    ما تیم های 5 لیگ برتر اروپایی رو بر اساس حضور داشتن یا نداشتن در لیگ قهرمانان به دو دسته تفسیم کردیم
        .در این دو گروه ویژگی های گل های زده و خورده و همچنین امتیاز  تیم‌ها را بررسی کردیم
    

    :فزضیه ما بر اساس دلیل زیر درست است

    اینکه تعداد گل های دریافتی در تیم های حاضر در لیگ کمتر بوده و به طور کلی دفاع بهتری نسبت به سایر تیم‌ها دارند
    و همچنین تعداد گل های زده در تیم های حاضر در لیگ بیشتر بوده و به طور کلی حمله بهتری نسبت به سایر تیم‌ها دارند
    از دو مورد بالا و همچنین نتایج و امتیازات بدست آمده در لیگ می توان نتیجه گرفت که این تیم ما به طور کلی بهتر  از تیم های دیگر در لیگ خود عمل میکنند
    </div>
    """, unsafe_allow_html=True)



def third_hypo():
    st.markdown("""
        <div style="text-align: right;">
            بازیکنانی که حداقل در ۲۰ درصد از بازی‌های تیم شرکت کرده‌اند، فعال حساب می‌شوند. در صورتی که میانگین سنی بازیکنان تیم بیشتر شود، تعداد بازیکنان فعال نیز بیشتر می‌شود.
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    with st.echo():
        with open('transfermarkt_clubs_seasonal.csv', 'r') as f:
            clubs = pd.read_csv(f)

        with open('Result_8.csv', 'r') as f:
            players = pd.read_csv(f)
        all_stat = pd.DataFrame()
        all_stat = clubs.merge(players, on='club_id', how='inner')

        all_stat.fillna(0, inplace=True)
        all_stat['appearances'] = ((all_stat['games_played']/all_stat['total_games']) * 100).astype(int)

        # group the teams by their average age to 5 groups
        all_stat['age_level'] = pd.cut(all_stat['avg_age'], bins=5, labels=[1, 2, 3, 4, 5])

        old_teams = all_stat[all_stat['age_level'] > 3]['appearances'].mean()
        young_teams = all_stat[all_stat['age_level'] < 3]['appearances'].mean()
        st.write("old teams appearances: ", old_teams)
        st.write("young teams appearances: ", young_teams)
    st.write("")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
        در این تست فرض ما به این نتیجه رسیدیم که در تیم هایی که میانگین سنی بالا تری دارند ، درصد حضور همه بازیکن در زمین افزایش میابد

    :دلایل درستی فرض
    
    نا توان بودن بازیکنن پیر تر در حضور در بازی به طور کامل است
        از طرفی این بازیکنان به دلیل تجربه بالا از طرف مربیان به زمین فرستاده می شوند تا بازیکنان کم تجربه از آنها یاد بگیرند
        حضور بازیکنان با تجربه در کنار بازیکنان کم تجربه امکان انتقال سبک و نوع بازی تیم به این بازیکنان را بیشتر میکند
    </div>
    """, unsafe_allow_html=True)



def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def desc_stat():
    st.markdown("""
    <div style="text-align: right;">
        توزیع تعداد بازی‌هایی که بازیکنان در یک فصل انجام می‌دهند را به دست بیاورید. هم‌چنین نشان دهید که بازیکنان در چند درصد از بازی‌ها شرکت کرده‌اند.
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('tosifi1.png')
    st.image(image,caption="Appearance counts distribution")
    st.write("")
    st.write("")
    st.write("")



    st.write("---")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
        بررسی کنید که‌ چه ارتباطی بین تعداد گل‌های زده‌شده و قیمت تخمینی سایت برای یک بازیکن وجود دارد (برای این کار از رگرسیون خطی استفاده کنید)
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('tosifi2.png')
    st.image(image,caption="Market Value by Goals for all players")
    st.write("")


    st.write("---")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
        بررسی کنید که‌ چه ارتباطی بین تعداد گل‌های زده‌شده و قیمت تخمینی سایت برای یک مهاجم وجود دارد (برای این کار از رگرسیون خطی استفاده کنید)
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('tosifi3.png')
    st.image(image,caption="Market Value by Goals for attack (forward) players")
    st.write("")

    st.write("---")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
        توزیع قیمت تخمینی بازیکنان را با تفکیک پست بازیکنان به دست بیاورید
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('tosifi4.png')
    st.image(image,caption="Market Value distribution by Positions")
    st.write("")

    st.write("---")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
        تعداد گل‌های زده‌شده در لیگ‌های مختلف را بدست آورید
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('tosifi5.png')
    st.image(image,caption="Goals distribution by Leagues")
    st.write("")

    st.write("---")
    st.write("")
    st.markdown("""
    <div style="text-align: right;">
        توزیع میزان هزینه‌ای که تیم‌ها در هر فصل برای خرید بازیکنان داشته‌اند را به‌دست بیاورید
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    image = Image.open('tosifi6.png')
    st.image(image,caption="Seasonal players' cost for clubs")
    st.write("")


lottie_url_download = "https://assets6.lottiefiles.com/packages/lf20_22mjkcbb.json"

lottie_download = load_lottieurl(lottie_url_download)

col1,col2,col3 = st.columns([1,3,1])
with col2:
    st.title('Statistical Analysis')

st_lottie(lottie_download, key="hello",speed=1, loop=True, quality="medium", width=700,height=400)




selector = st.selectbox('Select your desired analysis',("Descriptive Statistics", "Expert's Request","Players Request","Coach's Request", "First Hypothesis", "Second Hypothesis", "Third Hypothesis"))


if selector == "Descriptive Statistics":
    st.title(selector)
    desc_stat()
elif selector == "Expert's Request":
    st.title(selector)
    exp_req()
elif selector == "Players Request":
    st.title(selector)
    player_req()
elif selector == "Coach's Request":
    st.title(selector)
    coach_req()
    
elif selector == "First Hypothesis":
    st.title(selector)
    first_hypo()

elif selector == "Second Hypothesis":
    st.title(selector)
    sec_hypo()

elif selector == "Third Hypothesis":
    st.title(selector)
    third_hypo()






def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("pages.css")
