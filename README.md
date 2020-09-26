![](https://i.imgur.com/bhZ9Y7z.png)

A data pipeline to analyze Chess.com's [Puzzle Rush Leaderboard](https://www.chess.com/leaderboard/rush?type=hour). 

- [About](#about)
- [Purpose](#purpose)
- [Inspiration](#inspiration)
- [Data pipeline](#data-pipeline)
  - [Web scraping](#web-scraping)
  - [Create user profiles](#create-user-profiles)
  - [Store data](#store-data)
  - [Query data](#query-data)
  - [Analyze & Communicate](#analyze--communicate)
- [TODO:](#todo)

# About
Puzzle Rush challenges players to solve chess puzzles as quickly as possible. The rules are simple:
   - Solve as many puzzles as you can in the allotted time,
   - Puzzles get harder the more you solve,
   - Three strikes and you're out!


# Purpose
The purpose of this data pipeline is to determine the best time to play Puzzle Rush to place #1 on the Global Hourly Leaderboard.


# Inspiration 
Puzzlerush leaderboard ratings vary tremendously over time; ranging from an all-time high of [91](https://www.chess.com/member/spicycaterpillar) to scores as low as 35 on the Global Hourly Leaderboard. 

My interest in this data pipeline emerged when I accidentally placed 5th on the Puzzle Rush Global Leaderboard. Now, I am interested to place in the top 3 on the Global Leaderboard.

![](https://i.imgur.com/3wMZI6N.png)





# Data pipeline
There are 5 steps in this data pipeline:
   1. Web scraping: retrieve the users and ratings on the global hourly leaderboard.
   2. Create user profiles: Connect to chess.com's API and retrieve user information for fun, exploratory data analysis.
   3. Store data: store the data in an online database.
   4. Query data: query the data from the online database.
   5. Analyze & Communicate: analyze the data and display results on an interactive(?) dashboard.

> TODO: - Create data pipeline graphic w/ pictures of technologies used.

## Web scraping
LeaderboardScraper class uses selenium to retrieve usernames and scores from chess.com. Cleans data and returns a list of tuples containing the username and their puzzle rush score.

## Create user profiles
Creates User classes for each username on Leaderboard. Connects to chess.com's API to retrieve user information for exploratory data analysis. UserSaver class writes player profiles to csv file.

## Store data
WIP

## Query data
WIP

## Analyze & Communicate
WIP


# TODO:
_note_ may alternatively like to run the script locally via windows task setter for preliminary implementation.

1. Research online databases to save to
   1. potentially Lambda & DynamoDB...
1. Deploy script online to run every X minutes 
1. Test data collected & stored as intended
1. Research dashboard stuff...
