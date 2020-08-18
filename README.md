# Puzzle Rush Leaderboard Data Pipeline
This repo contains code for a data pipeline to analyze chess.com's [puzzle rush leaderboards](https://www.chess.com/leaderboard/rush?type=hour). 


## Inspiration 

Chess.com's Puzzlerush leaderboard ratings vary tremendously over time; ranging from an all-time high of 91 by GM [Ray Robson](https://www.chess.com/member/spicycaterpillar) to scores as low as 35 on the Global Hourly Leaderboard. The purpose of this data pipeline is to determine the best time to play Puzzle Rush to place #1 on the Global Hourly Leaderboard.

> Add interest from accidentally placing on LB


## Data pipeline
There are 5 steps in this data pipeline:
   1. Web scraping: retrieve the users and ratings on the global hourly leaderboard.
   2. Create user profiles: Connect to chess.com's API and retrieve user information for fun, exploratory data analysis.
   3. Store data: store the data in an online database.
   4. Query data: query the data from the online database.
   5. Analyze & Communicate: analyze the data and display results on an interactive(?) dashboard.

> TODO: - Create data pipeline graphic w/ pictures of technologies used.


### Web scraping


### Create user profiles

### Store the data

### Store data

### Query data

### Analyze & communicate


## TODO:
1. Re-structure clean user attribute functions (datetimes, location non commas)
2. Modulate scraping module.
3. Implement remote Selenium
4. Research online databases to save to
   1. potentially Lambda & DynamoDB...
5. Deploy script online to run every X minutes 
   1. 1? 3? 5?
6. Test data collected & stored as intended
7. Research dashboard stuff...


