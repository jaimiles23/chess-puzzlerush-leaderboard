"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-16 13:47:49
 * @modify date 2020-08-16 17:39:30
 * @desc [
    Main script to find chess.com ratings for user profiles.

    Steps:
        1. Imports
        2. Webscrape puzzle rush leaderboard
        3. Create user profiles with stats
        4. Convert user profiles to be saved
        5. Write to csv
 ]
 */
"""

##########
# Imports
##########

import logging
import time

from scraping import LeaderboardScraper
from user_class import User
from user_class import UserSaver


##########
# Logging
##########

logger = logging.getLogger(__name__ + "main")
logger.setLevel(10)


##########
# Main Scripts
##########

def main():
    
    logging.info("1.  Webscraping")
    usernames_scores = LeaderboardScraper.get_usernames_scores()


    logging.info("2.  Create user profiles")
    user_profiles = []
    for username, score in usernames_scores:
        user_profiles.append( User(username, score))


    logging.info("3.  Save user profiles")
    UserSaver.write_users_to_csv(user_profiles)


##########
# main == name
##########

if __name__ == "__main__":
    runs = 20
    minutes_between_runs = 5

    for i in range(runs):
        main()
        time.sleep(minutes_between_runs * 60)

