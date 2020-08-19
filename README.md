
# Puzzle Rush Leaderboard Data Pipeline
This repo contains code for a data pipeline to analyze chess.com's [puzzle rush leaderboards](https://www.chess.com/leaderboard/rush?type=hour). 


## Inspiration 

Chess.com's Puzzlerush leaderboard ratings vary tremendously over time; ranging from an all-time high of [91](https://www.chess.com/member/spicycaterpillar) to scores as low as 35 on the Global Hourly Leaderboard. The purpose of this data pipeline is to determine the best time to play Puzzle Rush to place #1 on the Global Hourly Leaderboard.

> Add interest from accidentally placing on LB


## Data pipeline
There are 5 steps in this data pipeline:
   1. Web scraping: retrieve the users and ratings on the global hourly leaderboard.
   2. Create user profiles: Connect to chess.com's API and retrieve user information for fun, exploratory data analysis.
   3. Store data: store the data in an online database.
   4. Query data: query the data from the online database.
   5. Analyze & Communicate: analyze the data and display results on an interactive(?) dashboard.

> TODO: - Create data pipeline graphic w/ pictures of technologies used.


1. Web scraping:
   1. LeaderboardScraper class uses selenium to retrieve usernames and scores from chess.com. Cleans data and returns a list of tuples containing the username and their puzzle rush score.
2. Create user profile:
   1. Creates User classes for each username on Leaderboard. Connects to chess.com's API to retrieve user information for exploratory data analysis. UserSaver class writes player profiles to csv file.
3. Store data
   1. 



### Store data


### Query data


### Analyze & communicate


## TODO:
1. Fix user class to include all attr even if not included in dict.
2. Implement remote Selenium
3. Research online databases to save to
   1. potentially Lambda & DynamoDB...
4. Deploy script online to run every X minutes 
   1. 1? 3? 5?
5. Test data collected & stored as intended
6. Research dashboard stuff...


