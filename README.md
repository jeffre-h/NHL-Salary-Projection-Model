# NHL Salary Projection Machine Learning Model

## 1. Defining the Problem
Every player in the NHL has a contract and the salary compensation they receive is dependent on a myriad of variables. So much so that predicting NHL salaries is a virtually impossible task. The goal is to make the best predictions we can using various regression models.  A useful application of this prediction model is to view predictions as projections for how much a player should actually make. Meaning if a player’s actual salary is greater than the predicted salary, then we can view this player as “overpaid”. Conversely, if a player’s actual salary is less than the predicted salary, we can view the player as “underpaid”.



## 2. Data Acquisition
Because of the amount and variety of stats needed, data was acquired from 2 sources:
1) hockey-reference.com : on-ice stats, advanced stats for goalies
2) capfriendly.com : advanced stats for skaters, physical attributes & contract information

The hockey-reference data was easy to acquire as they provided a downloadable csv for each hockey season on their website. Additionally, the hockey-reference website already had the skater and goalie data separated. 

The Capfriendly website on the other hand took a significantly longer time to acquire. They did not provide a downloadable csv file and only displayed stats for 50 players at a time. Thus to extract the data for a season, one would have to scrape 50 players at a time using excel and its “import from web” feature. The dataset was then split into skaters and goalies afterwards.



## 3. Data Cleaning & Preperation

For the Capfriendly datasets, the “01-cleaning_cf.py” script is used to clean the raw data collected:
```bash
python3 01-cleaning_cf.py raw/2018-2019/capfriendly1819.csv cleaned/2018-2019
python3 01-cleaning_cf.py raw/2019-2020/capfriendly1920.csv cleaned/2019-2020
python3 01-cleaning_cf.py raw/2020-2021/capfriendly2021.csv cleaned/2020-2021
python3 01-cleaning_cf.py raw/2021-2022/capfriendly2122.csv cleaned/2021-2022
python3 01-cleaning_cf.py raw/2022-2023/capfriendly2223.csv cleaned/2022-2023
```
First, player names were formatted such that there was a numerical identifier before a players name. For example: “1. Connor McDavid'' or “191. Thatcher Demko''. To resolve this, the use of regular expressions is needed to return a substring only containing the player name. This was a crucial step as player names are the unique identifiers used when joining the 2 datasets later. Next, quantifying draft positions. A player selected 1st overall in the draft would have the value “1” and any undrafted player would have a value of “300”. Next, filtering out entry-level contracts (ELC’s) and contracts signed by players 35 or older because these contracts are structured in a way that is favourable for NHL teams. As a result, these contracts are, for the most part, not indicative of a player’s projected contract value and would be considered in our datasets. Lastly, separating the data into 2 separate datasets for players and dropped columns in the goalie datasets that were only applicable to skaters.

For the Hockey-Reference datasets, the “01-cleaning_hr.py” script is used to clean the raw data collected:
```bash
python3 01-cleaning_hr.py raw/2018-2019/hockeyref1819.csv raw/2018-2019/hockeyref_goalie1819.csv cleaned/2018-2019
python3 01-cleaning_hr.py raw/2019-2020/hockeyref1920.csv raw/2019-2020/hockeyref_goalie1920.csv cleaned/2019-2020
python3 01-cleaning_hr.py raw/2020-2021/hockeyref2021.csv raw/2020-2021/hockeyref_goalie2021.csv cleaned/2020-2021
python3 01-cleaning_hr.py raw/2021-2022/hockeyref2122.csv raw/2021-2022/hockeyref_goalie2122.csv cleaned/2021-2022
python3 01-cleaning_hr.py raw/2022-2023/hockeyref2223.csv raw/2022-2023/hockeyref_goalie2223.csv cleaned/2022-2023
```
The bulk of the cleaning was filtering out players with insufficient games played. We simply asserted that skaters who don’t play at least half the games in a season (41) would be filtered out of the dataset for that season. Goalies follow a different dynamic, so we asserted that goalies who didn’t play at least 10 games in a season would be filtered out from the dataset. Any amount of games played less than this threshold, would indicate that the player is a fringe “NHLer” and would not be a useful datapoint. Lastly, we had to reduce these thresholds from 41 to 28 and 10 to 7 for the 2019-2020 season, which was shortened to 56 games due to covid-19.

After cleaning the datasets from both sites, we wrote the “02-combine_data.py” script to join the datasets on player names for each year. 

For skaters:
```bash
python3 02-combine_data.py cleaned/2018-2019/1819_cf_s.csv cleaned/2018-2019/1819_hr_s.csv combined
python3 02-combine_data.py cleaned/2019-2020/1920_cf_s.csv cleaned/2019-2020/1920_hr_s.csv combined
python3 02-combine_data.py cleaned/2020-2021/2021_cf_s.csv cleaned/2020-2021/2021_hr_s.csv combined
python3 02-combine_data.py cleaned/2021-2022/2122_cf_s.csv cleaned/2021-2022/2122_hr_s.csv combined
python3 02-combine_data.py cleaned/2022-2023/2223_cf_s.csv cleaned/2022-2023/2223_hr_s.csv combined
```
For goalies:
```bash
python3 02-combine_data.py cleaned/2018-2019/1819_cf_g.csv cleaned/2018-2019/1819_hr_g.csv combined
python3 02-combine_data.py cleaned/2019-2020/1920_cf_g.csv cleaned/2019-2020/1920_hr_g.csv combined
python3 02-combine_data.py cleaned/2020-2021/2021_cf_g.csv cleaned/2020-2021/2021_hr_g.csv combined
python3 02-combine_data.py cleaned/2021-2022/2122_cf_g.csv cleaned/2021-2022/2122_hr_g.csv combined
python3 02-combine_data.py cleaned/2022-2023/2223_cf_g.csv cleaned/2022-2023/2223_hr_g.csv combined
```
In doing so, we had to consider cases where 2 different players had the exact same name. From 2018-2023, we found that there were 2 instances. The first instance being “Sebastian Aho”, who are both skaters. The second instance being “Matt Murray”, who are both goalies. In both cases, one of the players did not meet the games played threshold used during data cleaning and were filtered out of our cleaned dataset. 



## 4. Data Analysis

```bash
python3 03-analysis_skaters.py
```

```bash
python3 04-analysis_goalies.py
```

The data is then split into a training set and a test set and applied to various regression models. The training set for the data was a combination of the data sets from the 2018-209 season to the 2021-2022 season and the test data set was the 2022-2023 season set. The data was applied to five common regression models, including Random Forest, Gradient Boosting, MPL, and K neighbor. Of these options, Random Forest and Gradient Boosting performed the best throughout the analysis, so they were used in a voting regression model to predict the future cap hit percentage. Next, plot the predicted cap hit using the voting model against the actual cap hit percentage for the 2022-2023 season. 


## 5. Visualizations

Projected vs. Actual salaries for 2023 free agents. For more visualizations, all NHL players or strictly Canucks players, checkout the other files in the github,

### Centres
![centre_fa](https://github.com/jeffre-h/NHL_Salary_Projection_Machine_Learning_Model/assets/104662025/7169ad8c-775b-4258-b531-66ae22bdfd27)

### Wingers
![winger_fa](https://github.com/jeffre-h/NHL_Salary_Projection_Machine_Learning_Model/assets/104662025/9d5814f1-716e-435d-b4fc-71ba0ab4c683)

### Defencemen
![defence_fa](https://github.com/jeffre-h/NHL_Salary_Projection_Machine_Learning_Model/assets/104662025/f1c145bd-4ff3-412e-888c-9bb66bad4c01)

### Goaltenders
![goalie_fa](https://github.com/jeffre-h/NHL_Salary_Projection_Machine_Learning_Model/assets/104662025/c8e2c86d-0dc6-40fd-bfcb-f774d22456aa)

