"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-16 13:47:49
 * @modify date 2020-08-16 14:04:53
 * @desc [
    Main script to find chess.com ratings for user profiles.

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

import time


import bs4
from datetime import datetime
import json
import requests
from selenium import webdriver


from scraping import puzzlerush_leaderboard
from user_class.create_user import User



##########
# Main Scripts
##########

def main():
    
    ## Get leaderboard usernames & scores
    usernames_scores = puzzlerush_leaderboard.get_usernames_scores()

    ## Create user profiles
    user_profiles = []
    for username, score in usernames_scores:
        user_profiles.append( User(username, score))
    
    ## View user profiles
    for i in range(len(user_profiles)):
        print(i + 1, '\t', end = "")
        user_profiles[i].view_profile()

 


##########
# main == name
##########

if __name__ == "__main__":
    main()





