![](https://i.imgur.com/bhZ9Y7z.png)

A data pipeline to analyze Chess.com's [Puzzle Rush Leaderboard](https://www.chess.com/leaderboard/rush?type=hour). 

- [Purpose](#purpose)
- [About](#about)
- [Data pipeline](#data-pipeline)
  - [Web scraping](#web-scraping)
  - [Create user profiles](#create-user-profiles)
  - [Store data](#store-data)
  - [Query data](#query-data)
  - [Analyze & Communicate](#analyze--communicate)
- [TODO:](#todo)


# Purpose
This data pipeline is intended to determine the best time to play Puzzle Rush to place #1 on the Global Hourly Leaderboard.


# About
Puzzle Rush challenges players to solve chess puzzles as quickly as possible. The rules are simple:
   - Solve as many puzzles as you can in the allotted time,
   - Puzzles get harder the more you solve,
   - Three strikes and you're out!

The Global Hourly Leaderboard tracks the top Puzzle Rush scores in the last 60 minutes. The top ranking varies tremendously over time; ranging from an all-time high of [91](https://www.chess.com/member/spicycaterpillar) to more attainable scores like 35. The variation is likely because of time zones influencing differences in player activity.

My interest in this data pipeline emerged when I accidentally placed 5th on the Puzzle Rush Global Leaderboard.

![](https://i.imgur.com/3wMZI6N.png)

This data pipeline is intended to analyze the Puzzle Rush Hourly Leaderboard and determine the best time to optimize my chance to place #1 on the Global Leaderboard. I collect information from users on the Leaderboard including their country code and account statistics.


# Data pipeline
There are 5 steps in this data pipeline:
   1. **Web scraping**
      1. Retrieve the users and ratings on the global hourly leaderboard.
   2. **Create user profiles**
      1. Connect to chess.com's API and retrieve user information for fun, exploratory data analysis.
   3. **Store data**
      1. Store the data in an online database.
   4. **Query data**
      1. Query the data from the online database.
   5. **Analyze & Communicate**
      1. Analyze the data and display results on an interactive(?) dashboard.

> TODO: - Create data pipeline graphic w/ pictures of technologies used.


## Web scraping
The `LeaderboardScraper` class contains methods for web-scraping. Methods use Selenium to retrieve usernames and scores from the leaderboard, clean the data, and return a list of tuples containing the username and their puzzle rush score.


## Create user profiles
Instantiates `User` class for each username on Leaderboard. The `User` class creates a User object with information on the user's account via the chess.com API. The `UserSaver` class writes player profiles to a csv file.


## Store data
WIP - store data in online database

## Query data
WIP - query from online database

## Analyze & Communicate
WIP - create dashboard showing best time to play


# TODO:
_note_ may alternatively like to run the script locally via windows task setter for preliminary implementation.

- [ ] Research online databases to save to
  - [ ] potentially Lambda & DynamoDB...
- [ ] Deploy script online to run every X minutes 
- [ ] Test data collected & stored as intended
- [ ] Research dashboard stuff...
