"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-15 23:06:48
 * @modify date 2020-08-16 13:38:14
 * @desc [
    Contains player class to hold player's statistics.

    NOTE
    I process the chess.com API data itno a standardized form within each user profile.
    I select data that I may find relevant/interesting to analysis and standardize
    timestamps into str-datetime format.
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
# from typing import Union


from user_class.user_constants import UserConstants


##########
# User object
##########

class User(UserConstants):

    ##########
    # Class 
    ##########

    ########## Constants
    ## NOTE: Careful consideration of tuple data structure.
    # Even if single item, must still have comma after so 
    # script considers the structure iterable.

    user_url = "https://api.chess.com/pub/player/{}"
    user_stats_url = "https://api.chess.com/pub/player/{}/stats"
    user_count = 0

    timestamps_to_datetimes = (
        'joined',
        'date',
    )
    # modes_play = (
    #     "chess_blitz",
    #     "chess_bullet",
    #     "chess_daily",
    #     "chess_rapid",
    # )
    # modes_practice = (
    #     "tactics",
    #     "lessons",
    # )
    # modes_puzzle_rush = (
    #     "puzzle_rush",
    # )

    # ########## Data structures
    # """
    # Tuple data structures holding dict keys to acccess user info from chess.com API.

    # keys_info:
    #     - account info
    # keys_games:
    #     - chess_blitz
    #     - chess_bullet
    #     - chess_daily
    #     - chess_rapid
    # keys_practice:
    #     - tactics
    #     - lessons
    # keys_puzzlerush:
    #     - puzzle rush
    # keys_daily:
    #     - daily puzzles
    # """

    # keys_info = (
    #     'player_id',
    #     'username', 
    #     'country',
    #     'location', 
    #     'joined',
    #     'status',
    #     "is_streamer",
    # )
    # keys_games = (
    #     ( "last", 
    #         ("rating", "date")),
    #     ("best", 
    #         ("rating", "date")),
    #     ("record",
    #         ("win", "loss", "draw"))
    # )
    # keys_practice = (
    #     ("highest", 
    #         ("rating", "date")),
    # )
    # keys_puzzlerush = (
    #     ("best",
    #         ("total_attempts", "score")),
    #     ("daily", 
    #         ("total_attempts", "score"))
    # )
    # """
    # NOTE
    # Puzzle rush daily stats are not available if user has not yet played today.
    # Because users are scraped from puzzlerush scoreboard, this should not present an issue.
    """


    ########## Methods

    @classmethod
    def add_user(cls):
        """Increments user count."""
        cls.user_count += 1
    

    @classmethod
    def print_num_users(cls):
        """Prints number of users."""
        print(cls.user_count)


    ##########
    # Static Methods
    ##########
    
    ########## API access
    @staticmethod
    def get_chessAPI_json(webpage: str) -> dict:
        """Returns json dict from chess.com API webpage.
        """
        results = requests.get(webpage)

        attempts = 0
        while results.status_code != 200:
            time.sleep(1/5)
            results = requests.get(webpage)

            attempts +=1 
            if attempts == 5:
                raise Exception(f"Unable to connect to {webpage}!")
        
        return results.json()
    
    
    ########## Datetime
    @staticmethod
    def check_if_timestamp(key: str) -> bool:
        """Returns bool if value needs to be converted to str date.
        """
        if key in User.timestamps_to_datetimes:
            return True
        return False


    @staticmethod
    def convert_to_strtime(timestamp: int) -> str:
        """Returns string date from timestamp."""
        date_obj = datetime.fromtimestamp(timestamp)
        return date_obj.strftime("%Y/%m/%d %H:%M:%S")
    

    ##########Country

    @staticmethod
    def check_if_country(key: str) -> bool:
        """Returns bool if country key that needs to be shortened."""
        return key == "country"
    

    @staticmethod
    def parse_country(value: str) -> str:
        """Returns country code represented by 2-character ISO 3166 code.
        
        ISO 3166 code:
        https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

        Chess.com API format:
        https://api.chess.com/pub/country/{iso}

        NOTE: 
            - Can compare country tzs in data analysis.
        """
        url_base = "https://api.chess.com/pub/country/"

        if value.find(url_base) == -1:
            ## TODO: Add logger
            return None

        else:
            return value[-2:]        


    ########## Dictionay access
    @staticmethod
    def get_nested_stats(top_dict: dict, key_tuple: tuple) -> dict:
        """Returns values from top_dict that are specified in the key_tuple.
        """
        stats_dict = dict()

        for key, nested_key_tuple in key_tuple:
            for nested_key in nested_key_tuple:
                
                try:
                    nested_dict = top_dict.get(key, None)
                    value = nested_dict.get(nested_key, None)

                    if User.check_if_timestamp(nested_key):
                        value = User.convert_to_strtime(value)

                except (KeyError, AttributeError) as e:
                    # ## ADD LOGGER.
                    value = None
                    # print("#" * 10, e)
                    # print(top_dict, key_tuple, key, nested_dict, nested_key_tuple, nested_key, sep = "\n")
                    # value = None
                    pass

                new_key = '_'.join([key, nested_key])
                stats_dict[new_key] = value
        
        return stats_dict


    @staticmethod
    def get_mode_stats(
        user_stat_dict: dict,
        modes: tuple, 
        dict_key_structure: tuple
        ) -> list:
        """Returns list of dicts for each mode from the user's stats dict.

        params:
        > user_stat_dict: dict. User dictionary of all user statistics
        > modes: tuple. Modes to access from user_stat_dict.
        > dict_key_strucutre: tuple. Mapping of the dict keys in the mode dictionay.
        """
        all_mode_stats = []
        
        for mode in modes:
            mode_dict = user_stat_dict.get(mode, None)
            mode_stats = User.get_nested_stats(mode_dict, dict_key_structure)
            
            all_mode_stats.append(mode_stats)
        
        return all_mode_stats
        

    ##########
    # Instance
    ##########

    def __init__(self, username: str, score: int):
        """Initializes user instance with username and score.

        From username, accesses chess.com API and records stats on:
        - player info
        - player ratings
        - practice
        - puzzle rush
        - daily
        """

        ## Init args
        self.username = username
        self.score = score

        ## webpages & json
        self.user_url = User.user_url.format(self.username)
        self.user_stats_url = User.user_stats_url.format(self.username)
        self.user_info_dict = self.fetch_userinfo_dict()
        self.user_stats_dict = self.fetch_userstats_dict()

        ## info
        self.user_info = self.get_user_info()

        ## rating 
        self.blitz, self.bullet, self.daily, self.rapid = self.get_user_rating_stats()

        ## practice 
        self.tactics, self.lessons = self.get_user_practice_stats()

        ## puzzle rush
        self.puz_rush = self.get_user_puzzlerush_stats()

        ## increment user
        User.add_user()


    ########## Get dicts

    def fetch_userinfo_dict(self) -> dict:
        """Returns dict from user's chess.com API"""
        return User.get_chessAPI_json( self.user_url)
    

    def fetch_userstats_dict(self) -> dict:
        """Returns dict from user's chess.com stats API"""
        return User.get_chessAPI_json( self.user_stats_url)


    ########## Info

    def get_user_info(self) -> dict:
        """Returns user stats from an unnested dictionary."""
        user_info = dict()

        for key in User.keys_info:
            value = self.user_info_dict.get(key, None)

            if User.check_if_timestamp(key):
                value = User.convert_to_strtime(value)
            elif User.check_if_country(key):
                value = User.parse_country(value)

            user_info[key] = value

        return user_info
    

    ########## Mode stats (blitz, bullet, daily, rapid)

    def get_user_rating_stats(self) -> list:
        """Return list of dicts with stats for user's rating modes.

        Modes include:
            - blitz
            - bullet
            - daily
            - rapid
        """
        return User.get_mode_stats(
            self.user_stats_dict, 
            User.modes_play,
            User.keys_games
        )
        

    ########## Practice (tactics, lessons)
    def get_user_practice_stats(self) -> list:
        """Returns list of dicts with stats for user's practice modes.

        Practice modes include:
            - Tactics
            - Lessons
        """
        return User.get_mode_stats(
            self.user_stats_dict,
            User.modes_practice,
            User.keys_practice,
        )
    

    ########## Puzzle Rush
    def get_user_puzzlerush_stats(self) -> list:
        """Returns dict with stats for puzzle rush."""
        return User.get_mode_stats(
            self.user_stats_dict,
            User.modes_puzzle_rush,
            User.keys_puzzlerush
    
        )

    
    ########## View player profile
    def view_profile(self) -> None:
        """Prints attributes from the player profile for viewing."""
        items = (
            self.username, 
            self.score, 
            self.user_info['country'], 
            # self.user_info['location'],
            # self.bullet,
        )
        print(items, sep = "\t")




##########
# Main
##########

def main():
    username = "jaimiles23"
    score = 23

    jai = User(username, score)

    print("\n\n", "#" * 10, "Player Variables", "#" * 10, "\n\n")
    for k, v in vars(jai).items():
        print("", k, "-" * 5, v, sep = "\n" * 1)

    jai.view_profile()
    
    

if __name__ == "__main__":
    main()