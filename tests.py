"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-18 18:13:04
 * @modify date 2020-08-18 18:13:04
 * @desc [
    Tests for main script.
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
# Tests
##########

def test_user_profile_complete() -> bool:
    """
    Returns boolean if all users havea  complete profile.
    """
    logging.info("1.  Webscraping")
    usernames_scores = LeaderboardScraper.get_usernames_scores()

    logging.info("2.  Create user profiles")
    user_profiles = []
    for username, score in usernames_scores:
        user_profiles.append( User(username, score))


    # Determine which vars are NOT included in user attributes.
    ## 
    attr_dict = dict()
    for profile in user_profiles:
        
        for v in vars(profile):
            if v not in attr_dict.keys():
                attr_dict[v] = 1
            else:
                attr_dict[v] = attr_dict[v] + 1
    
    for k, v in attr_dict.items():
        print(k, '-', v)
        assert v == 50


##########
# Main Scripts
##########

def main():
    test_user_profile_complete()


##########
# main == name
##########

if __name__ == "__main__":
    main()

