import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests

st.set_page_config(
    page_title="Machine Learning",
    page_icon="🤖",
)


def mkv_pred():
    with st.echo():
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        import pandas as pd
        df = pd.read_csv("All_player_with_score.csv")
        df.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1, inplace=True)
        df_grouped = df.groupby('player_name').agg({'season_id': 'max', 'player_id': 'max','goals': 'max', 'assists': 'max','ppg': 'max', 'yellow_cards': 'max','second_yellow_cards': 'max', 'red_cards': 'max', 'height': 'max','foot': 'max', 'position': 'max','age': 'max', 'apprance': 'max','score': 'max', 'goals_conceded': 'max', 'clean_sheets': 'max' ,'mk_value': 'mean'}).reset_index()
        df_grouped.fillna(0, inplace=True)
        df_final = df.drop(['player_name','position','player_id', 'season_id', 'foot', 'agent','date_of_birth','height'], axis=1)
        df_final.fillna(0, inplace=True)
        st.write("")
        st.write("")
        st.dataframe(df_final)
        st.write("")
        st.write("")
    
    st.write("---")
    st.write("")
    st.write("")

    with st.echo():
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split

        X = df_final.drop("mk_value", axis=1)
        y = df_final["mk_value"]   


        X_train, X_valid , y_train, y_valid = train_test_split(X, y, test_size=.2)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)

    with st.echo():
        # from sklearn.neighbors import KNeighborsClassifier
        # from sklearn.model_selection import GridSearchCV
        
        # param_grid = {
        #     'n_neighbors': [1, 3, 5, 7, 9],
        #     'weights': ['uniform', 'distance'],
        #     'p': [1, 2],
        #     'algorithm': ['brute', 'kd_tree']
        # }

        # knn = KNeighborsClassifier()
        # grid_search = GridSearchCV(knn, param_grid, cv=5, verbose=True)
        # grid_search.fit(X_train_scaled, y_train)

        # best_params = grid_search.best_params_
        # print("Best parameters:", best_params)

        # best_model = grid_search.best_estimator_
        pass
    
    st.write("")
    st.write("")
    with st.echo():
        from sklearn.neighbors import KNeighborsClassifier
        model = KNeighborsClassifier(algorithm ='kd_tree', n_neighbors = 1, p = 1, weights = 'uniform')
        model.fit(X_train_scaled, y_train)
        from sklearn.metrics import r2_score
        prediction = model.predict(scaler.transform(X_valid))
        st.write("R2Score = ", r2_score(y_valid,prediction))


def player_class():
    with st.echo():
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        import pandas as pd

        df = pd.read_csv("All_player_with_score.csv")

        df.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1, inplace=True)

        df.replace(['Attacking Midfield', 'Central Midfield', 'Left Midfield','Right Midfield','Defensive Midfield','Defensive Midfield'], 'Midfiedld' ,inplace=True)
        df.replace(['Centre-Forward', 'Right Winger','Second Striker', 'Left Winger'], 'Attack' ,inplace=True)
        df.replace(['Left-Back', 'Centre-Back', 'Right-Back'], 'Defensive' ,inplace=True)


        df.fillna(0 ,inplace=True)
        df.drop('date_of_birth', axis=1 , inplace=True)


        df = df.drop_duplicates(['player_name']).reset_index()


        df.drop(['agent', 'foot','season_id','index','player_id','mk_value','ppg'], axis=1 , inplace=True)

        st.dataframe(df)
    
    
    st.write("")
    st.write("")
    with st.echo():
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder

        encoder = LabelEncoder().fit(df['position'])
        df['position'] =  encoder.transform(df['position'])



        df.drop('player_name' , axis=1 , inplace=True)

        from sklearn.model_selection import train_test_split
        X = df.drop('position' , axis=1)
        y = df['position']

        X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.2)

        from sklearn.preprocessing import StandardScaler
        ss = StandardScaler()
        X_train = ss.fit_transform(X_train)
        X_test =  ss.transform(X_test)
    
    
    st.write("")
    st.write("")
    with st.echo():
        # from sklearn.model_selection import GridSearchCV

        # rf = RandomForestClassifier()

        # param_grid = {
        #     'n_estimators': [100, 200, 300],
        #     'max_depth': [None, 5, 10],
        #     'min_samples_split': [2, 5, 10]
        # }

        # grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5 , verbose=True)
        # grid_search.fit(X_train,y_train)

        # print("Best Parameters:", grid_search.best_params_)
        # print("Best Score:", grid_search.best_score_)
        #------------------------------------------------------------------------------------------

        # from sklearn.svm import SVC
        # from sklearn.model_selection import GridSearchCV

        # sv = SVC(max_iter=1000000)

        # param_grid = {
        #     'C': [0.1, 1, 10],
        #     'kernel': ['linear', 'rbf'],
        #     'gamma': ['scale', 'auto']
        # }

        # grid_search = GridSearchCV(estimator=sv, param_grid=param_grid, cv=5 , verbose=True)
        # grid_search.fit(X_train,y_train)

        # print("Best Parameters:", grid_search.best_params_)
        # print("Best Score:", grid_search.best_score_)
        #------------------------------------------------------------------------------------------

        
        # from sklearn.linear_model import LogisticRegression
        # from sklearn.model_selection import GridSearchCV

        # lr = LogisticRegression(max_iter=100000)


        # param_grid = {
        #     'C': [0.1, 1, 10],
        #     'penalty': ['l1', 'l2'],
        #     'solver': ['liblinear', 'saga']
        # }

        # grid_search = GridSearchCV(estimator=lr, param_grid=param_grid, cv=5 , verbose=True)
        # grid_search.fit(X_train,y_train)

        # print("Best Parameters:", grid_search.best_params_)
        # print("Best Score:", grid_search.best_score_)    
        pass
    
    
    st.write("")
    st.write("")
    with st.echo():

        from sklearn.metrics import classification_report

        rf_best = RandomForestClassifier(max_depth=None , min_samples_split= 10 , n_estimators=300).fit(X_train,y_train)

        y_pred = rf_best.predict(X_test)

        st.write("accuracy score = ",accuracy_score( y_pred,y_test))
        st.write("")
        st.write("")
    
    st.write("")
    st.write("")
    with st.echo():
        st.write("classification report\n\n", classification_report(y_pred , y_test))
    
    st.write("")
    st.write("")
    with st.echo():
        import matplotlib.pyplot as plt 
        import seaborn as sns
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df, x='score', y='apprance', hue='position', ax=ax)
        plt.figure(figsize=(28, 6))
        st.pyplot(fig)




def player_cluster():
    with st.echo():
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        import pandas as pd
        import matplotlib.pyplot as plt 
        import seaborn as sns


        df = pd.read_csv("All_player_with_score.csv")
        st.dataframe(df)

    st.write("")
    st.write("")
    with st.echo():
        df.drop(['Unnamed: 0.1', 'Unnamed: 0','position', 'agent'], axis=1, inplace=True)
        df.fillna(0 ,inplace=True)
        df.drop('date_of_birth', axis=1 , inplace=True)

        df = df.drop_duplicates(['player_name']).reset_index()
        df_filterd = df.drop(['index', 'season_id', 'player_id','player_name'], axis=1)
    
        st.dataframe(df_filterd)

    st.write("")
    st.write("")    
    with st.echo():
        df_plt = df_filterd.drop('foot', axis=1)
        len_cols = len(df_plt.columns)
        fig_col = 3 
        fig_row = int(np.ceil(len_cols/fig_col))
        fig, ax = plt.subplots(nrows=fig_row, ncols=fig_col, figsize=(12,20))

        for i in range(len_cols) : 
            row_idx = int(i//fig_col)
            col_idx = int(i%fig_col)
            sns.boxplot(df_plt.iloc[:,i], ax = ax[row_idx][col_idx], palette='magma')
            ax[row_idx][col_idx].set_title(df_plt.columns[i])
    st.pyplot(fig)

    st.write("")
    st.write("")
    with st.echo():
        from sklearn.cluster import KMeans
        max_k = 15
        cost = []
        for i in range(1,max_k) : 
            m = KMeans(n_clusters=i, n_init=10, init='k-means++')
            m.fit(df_plt)
            cost.append(m.inertia_)
            
            
        fig, ax = plt.subplots()
        ax.plot(range(1, max_k), cost)
        ax.set_xlabel('Number of Clusters')
        ax.set_ylabel('Cost')
        ax.set_title('Elbow Method')
        st.pyplot(fig)

    st.write("")
    st.write("")    
    with st.echo():
        m = KMeans(n_clusters=3, n_init=10, init='k-means++')
        df_plt['cluster'] = m.fit_predict(df_plt)
        df_plt

    st.write("")
    st.write("")    
    with st.echo():
        from sklearn.decomposition import PCA

        X = df_plt.drop('cluster', axis=1)
        pca_transformer = PCA(n_components=2,)

        pca_transformer.fit(X)


        reduced_X = pca_transformer.transform(X)
        reduced_df = pd.DataFrame(reduced_X, columns=['col1', 'col2'])
        reduced_df['cluster'] = df_plt.cluster
        reduced_df
    
    st.write("")
    st.write("")    
    with st.echo():
        sns.set_style("whitegrid")  # You can choose different styles like "white", "darkgrid", "ticks", etc.
        sns.set_palette("Set2")
        fig, ax = plt.subplots(figsize=(20, 10))
        plt.figure(figsize=(20, 10))
        sns.scatterplot(data=reduced_df, x='col1', y='col2', hue='cluster', ax=ax)
        st.pyplot(fig)

    st.write("")
    st.write("")    
    with st.echo():
        df['cluster'] = df_plt.cluster
        df

    st.write("")
    st.write("")    
    with st.echo():
        for cluster in range(3):
            st.write(f"\nCluster {cluster}:")
            cluster_df = df[df["cluster"] == cluster]
            country_values = cluster_df["player_name"].unique()
            st.write("Countries:", country_values)





def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



lottie_url_download = "https://assets3.lottiefiles.com/packages/lf20_kUtZCR7Zyk.json"

lottie_download = load_lottieurl(lottie_url_download)

col1,col2,col3 = st.columns([1,3,1])
with col2:
    st.title('Machine Learning')


st_lottie(lottie_download, key="hello",speed=1, loop=True, quality="medium", width=700,height=400)



selector = st.selectbox('Select a model',("Market Value Prediction", "Classifying Players","Clustering Players Based on Similarities"))


if selector == "Market Value Prediction":
    st.title(selector)
    mkv_pred()
elif selector == "Classifying Players":
    st.title(selector)
    player_class()
elif selector == "Clustering Players Based on Similarities":
    st.title(selector)
    player_cluster()



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("pages.css")
