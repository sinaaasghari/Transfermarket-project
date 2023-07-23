# Transfermarkt Data Analysis Project

## Description

This project focuses on analyzing data from Transfermarkt, a popular website for football transfer information. The goal is to perform statistical analyses and train machine learning models using the scraped data.

The project begins with the data scraping process, where relevant information is extracted from Transfermarkt. To ensure compatibility with the analysis implementations, a well-defined database schema is designed. The scraped data is then stored in the database for further analysis.

The project encompasses the following steps:

1. **Scraping the Required Data**: This step involves extracting the necessary data from Transfermarkt using web scraping techniques. Various attributes such as player details, transfer history, and team information are collected.

2. **Design, Implementation, and Storage of Data in the Database**: A suitable database schema is designed to accommodate the scraped data. This schema is implemented, and the collected data is stored in the database for efficient querying and analysis in subsequent steps.

3. **Statistical Analyses**: The collected data is subjected to various statistical analyses to gain insights and uncover patterns. This may include calculating player statistics, team performance metrics, transfer trends, or any other relevant analysis.

4. **Machine Learning Model Training**: Building upon the statistical analyses, machine learning models are developed to predict specific outcomes or make informed decisions based on the available data. This step involves feature engineering, model selection, training, and evaluation.

- This project contains a dashboard file that provides a comprehensive overview of the project. The dashboard can be accessed by running the `run_dashboard.py` file located in the `Transfermarkt-Dashboard` folder.

To run the dashboard, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the `Transfermarkt-Dashboard` folder.
3. Ensure that you have all the necessary dependencies installed (`pip install -r requirements.txt`).
4. Open a terminal or command prompt in the `Transfermarkt-Dashboard` folder.
5. Open `run_dashboard.py` or run the following command to start the dashboard:

```bash
python run_dashboard.py
```

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:
```bash
git clone git@github.com:sinaaasghari/Transfermarket-project.git
```

2. Install the necessary dependencies:
``` bash
pip install -r requirements.txt
```
3. Scraping the Required Data:

    Steps:

    - Scraping the seasons and countries data.
    - Scraping the leagues data based on seasons and countries and unique information for each league.
    - Scraping the clubs data based on seasons and leagues and unique information for each club.
    - Scraping the players data based on seasons and clubs and unique information (performances) for each player.
    - Scraping the transfer data for each of the players.
    - Scraping the data of the clubs' appearance in the 2021 Champions League.

- Modify the scraping script (all .py files in `Scrapping data` folders ) to specify the desired data to be collected.
- Run the script to scrape the data from Transfermarkt.
- The scraped data will be stored in the database for further analysis.

4. Design, Implementation, and Storage of Data in the Database:
- Set up a database system (e.g., MySQL, PostgreSQL) and create a new database for the project.
- open (`tmdb.py`) and in line **117 , 144** replace your username and in line **118,145** replace your password.
- Run the database creation script (`tmdb.py`) to generate the necessary tables and schema.


5. Statistical Analyses:
- We worked on three requests and three Hypothesis, each of which was handled in a separate file.

6. Machine Learning Model Training:
- The ML section of the bootcamp project involves using machine learning techniques to estimate and classify data from `transfermarkt.com`.
## Contribution

Contributions are welcome! If you find any issues or have suggestions for improvements, please submit an issue or a pull request. Let's collaborate and make this project even better.

## Acknowledgments

- The Transfermarkt website for providing valuable data for analysis.
- Open-source libraries and frameworks used in this project.
-  [*Sina Asghari*](https://github.com/sinaaasghari) and [*ArsalanMoravvej*](https://github.com/ArsalanMoravvej), [*Sina Saberi*](https://github.com/ssinasaberii), [*Mohammad Norasteh*](https://github.com/houman-nr) for their contributions and efforts in developing this project.
