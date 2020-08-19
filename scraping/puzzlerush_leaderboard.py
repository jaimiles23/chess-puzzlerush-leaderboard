"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-02 18:50:10
 * @modify date 2020-08-02 18:50:10
 * @desc [
   Script to scrape chess.com puzzle rush high scores.

   NOTE:
   requests isn't returning the full html and urllib is blocked.
   try to use selenium: 
   https://automatetheboringstuff.com/chapter11/
   https://selenium-python.readthedocs.io/installation.html

   Can also try to DOWNLOAD the webpage in html?? see if format is different?
   Or save the webpage as a pdf, and then use pdf identifier??

   TODO: 
   
    Move to remote-webdriver so doesn't have to run from desktop
    https://selenium-python.readthedocs.io/getting-started.html#selenium-remote-webdriver

    Try using requests-html instead
    https://requests.readthedocs.io/projects/requests-html/en/latest/#javascript-support
 
    If both methods work - use timeit and compare practicality.
 ]
 */
"""


##########
# Imports
##########

import logging
import time  


from selenium import webdriver
from typing import Tuple, List


from scraping.logger import logger



##########
# Type Hinting
##########

UsernameScore = Tuple[str, int]
UserameScore_List = List[UsernameScore]


##########
# LeaderboardScraper
##########

class LeaderboardScraper():
    """
    Contains methods & constants to scrape chess.com puzzle rush leaderboard.
    """

    ##########
    # Constants
    ##########

    webpage = "https://www.chess.com/leaderboard/rush?type=hour"


    ##########
    # Static Methods
    ##########

    @staticmethod
    def get_usernames_scores() -> UserameScore_List:
        """Returns list of UsernameScore tuples.

        TODO: Make each section into different functions??
        """

        def _get_elements( class_name: str) -> list:
            """Auxiliary method to get list of elements with class_name."""

            for _ in range(5):
                output = driver.find_elements_by_class_name(class_name)
                if len(output):
                    return output
                
                logger.info("Trying to connect again...")
                time.sleep(0.1)     # Table may not load immediately, try 5x
            
            raise Exception("Could not locate elements!")


        ##### Driver
        driver = webdriver.Firefox()
        driver.get(LeaderboardScraper.webpage)


        ##### User name
        username_class = "user-username-component"
        usernames = _get_elements(username_class)


        ##### Scores

        ## get scores
        score_class = "table-text-right"
        scores = _get_elements(score_class)

        ## clean scores
        # initial table text is rating.
        if scores[0].text == "Rating":
            del scores[0]
        else:
            print(scores[0].text)
            raise Exception("Rating text not found")

        num_removed = 0
        for i in range(len(scores)):
            if scores[i - num_removed].text[0] == "#":
                del scores[i - num_removed]
                num_removed += 1


        ##### Usernames_scores tuple
        assert len(usernames) == len(scores)

        usernames_scores = []
        for i in range(len(usernames)):
            entry = ( usernames[i].text, scores[i].text)
            usernames_scores.append(entry)

        driver.quit()
        return usernames_scores


##########
# Main
##########

def main():
    usernames_scores = LeaderboardScraper.get_usernames_scores()
    
    for user, score in usernames_scores:
        print(f"{user}\t{score}")


if __name__ == "__main__":
    main()
