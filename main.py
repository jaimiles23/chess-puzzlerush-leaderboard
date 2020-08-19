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


from scraping.puzzlerush_leaderboard import LeaderboardScraper
from user_class.user import User
from user_class.user_saver import UserSaver


##########
# Logging
##########

logger = logging.getLogger(__name__ + "main")


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


    ## Determine which vars are NOT included in user attributes.
    ## 
    attr_dict = dict()
    for profile in user_profiles:
        profile.view_profile(full=True)

        for v in vars(profile):
            if v not in attr_dict.keys():
                attr_dict[v] = 1
            else:
                attr_dict[v] = attr_dict[v] + 1


    ## print dict w/ counts
    for k, v in attr_dict.items():
        print(k, v, sep = "\t")
    
    


    logging.info("3.  Save user profiles")
    UserSaver.write_users_to_csv(user_profiles)


##########
# main == name
##########

if __name__ == "__main__":
    main()

