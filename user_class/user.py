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

    https://stackoverflow.com/questions/44813122/writing-list-of-objects-to-csv-file
 ]
 */
"""


##########
# Imports
##########

import time


import bs4
import csv
from datetime import datetime
import json
import pandas as pd
import requests
from typing import Tuple, Union, List

try:
    from user_class.user_constants import UserConstants
except:
    from user_constants import UserConstants


##########
# Types
##########

AttrInfo = Tuple[str, Union[str, int]]
AttrInfoList = List[AttrInfo]

KeyTuple = Tuple[str, tuple]


##########
# User object
##########

class User(UserConstants):

    ##########
    # Class 
    ##########
    user_count = 0


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


    ########## AttrInfoList
    """
    Helper methods to create AttrInfoList from user dictionaries.

    AttrInfo: (str, Union[str, int, float]). 
        AttrsInfo[0] represents the user's attribute
        AttrsInfo[1] represents the user's info
    """
    @staticmethod
    def get_attrinfolist(top_dict: dict, key_tuple: tuple, mode: str) -> AttrInfoList:
        """Returns list of (attr, info) from top_dict which are specified in the key_tuple.

        NOTE: Consider more flexible solutions - recursion/iteration
        """
        attr_info_list = list()

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


                new_key = '_'.join([mode, key, nested_key])
                attr_info_list.append( (new_key, value))
        
        return attr_info_list


    @staticmethod
    def get_mode_attrinfolist(
        user_stat_dict: dict,
        modes: tuple, 
        dict_key_structure: KeyTuple
        ) -> AttrInfoList:
        """Returns user's list of AttrInfoList  for each mode.

        params:
        > user_stat_dict: dict. User dict of all user statistics
        > modes: tuple. Modes to access from user_stat_dict.
        > dict_key_strucutre: tuple. Mapping of the dict keys in the mode dictionay.
        """
        attr_info_list = []
        
        for mode in modes:
            mode_dict = user_stat_dict.get(mode, None)
            if not mode_dict:       # User hasn't played mode.
                continue

            attr_info = User.get_attrinfolist(mode_dict, dict_key_structure, mode)
            attr_info_list.append(attr_info)
        
        return attr_info_list
    

    ##########
    # Instance
    ##########

    def __init__(self, username: str, score: int):
        """Initializes user instance with username and score.

        From username, accesses chess.com API and records info on:
        - player info
        - player ratings
        - practice
        - puzzle rush
        - daily
        """
        ## First, then later set by set_attrinfo_userinfo()
        self.player_id = None

        ## Init args
        self.username = username
        self.score = str(score)

        ## webpages & json
        self.user_url = User.user_url.format(self.username)
        self.user_stats_url = User.user_stats_url.format(self.username)
        self.user_info_dict = self.fetch_userinfo_dict()
        self.user_stats_dict = self.fetch_userstats_dict()

        ## info
        self.set_attrinfo_userinfo()

        ## Mode attrs
        self.set_attrinfo_ratings()
        self.set_attrinfo_practice()
        self.set_attrinfo_puzzlerush()

        ## increment user
        User.add_user()

        ## clean attr
        self.__delattr__('user_info_dict')
        self.__delattr__('user_stats_dict')


    ########## Add Attr Info
    """
    Helper methods to set user instance attributes from AttrInfoList.
    """

    def set_attrinfo_per_mode(self, attrinfolist_modes: list) -> None:
        """Sets the attribute info for each mode in AttrInfoList.
        """
        for attrinfo_list in attrinfolist_modes:
            self.set_attrinfo(attrinfo_list)
        
        return


    def set_attrinfo(self, attrinfo_list: AttrInfoList) -> None:
        """Sets self.attr for each attr, info in list.
        """
        for attr, info in attrinfo_list:
            setattr(self, attr, str(info))
        
        return


    ########## Get user info dicts

    def fetch_userinfo_dict(self) -> dict:
        """Returns dict from user's chess.com API"""
        return User.get_chessAPI_json( self.user_url)
    

    def fetch_userstats_dict(self) -> dict:
        """Returns dict from user's chess.com stats API"""
        return User.get_chessAPI_json( self.user_stats_url)


    ########## User information

    def set_attrinfo_userinfo(self) -> None:
        """Sets user information attributes."""
        user_info_attrinfo_list = self.get_attrinfolist_userinfo()

        self.set_attrinfo(user_info_attrinfo_list)
        return


    def get_attrinfolist_userinfo(self) -> AttrInfoList:
        """Returns AttrInfoList (str, Union) of user info from dictionary."""
        user_info_attrinfo_list = []

        for key in User.keys_info:
            value = self.user_info_dict.get(key, None)

            if User.check_if_timestamp(key):
                value = User.convert_to_strtime(value)
            elif User.check_if_country(key):
                value = User.parse_country(value)

            user_info_attrinfo_list.append( (key, value))

        return user_info_attrinfo_list
    
    
    ########## Mode info (blitz, bullet, daily, rapid)

    def set_attrinfo_ratings(self) -> None:
        """Sets user attributes for different rating modes.

        Modes include:
            - blitz
            - bullet
            - daily
            - rapid
        """

        ratings_attrinfo_list = User.get_mode_attrinfolist(
            self.user_stats_dict, 
            User.modes_play,
            User.keys_games
        )

        self.set_attrinfo_per_mode(ratings_attrinfo_list)
        return
        

    ########## Practice (tactics, lessons)

    def set_attrinfo_practice(self) -> list:
        """Sets user's attributes for practice modes.

        Practice modes include:
            - Tactics
            - Lessons
        """
        practice_attrinfo_list = User.get_mode_attrinfolist(
            self.user_stats_dict,
            User.modes_practice,
            User.keys_practice,
        )

        self.set_attrinfo_per_mode(practice_attrinfo_list)
        return
    

    ########## Puzzle Rush

    def set_attrinfo_puzzlerush(self) -> list:
        """Sets user's attributes for puzzle rush.
        
        TODO:
        - Currently returning list? Only structur difference is modes_puzzle_rush is single value. 
        - Investigate why & remove 0 index reference.
        """
        puzzlerush_attrinfo_list = User.get_mode_attrinfolist(
            self.user_stats_dict,
            User.modes_puzzle_rush,
            User.keys_puzzlerush
        )
        self.set_attrinfo_per_mode(puzzlerush_attrinfo_list)
        return

    
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

def instantiate_user():
    username = "jaimiles23"
    score = 23

    jai = User(username, score)
    return jai


def test_user_class(jai):

    print("\n\n", "#" * 10, "Player Variables", "#" * 10, "\n\n")

    # jai.view_profile()
    for v in vars(jai):
        print(v, getattr(jai, v))

    return


def main():
    jai = instantiate_user()
    test_user_class(jai)


if __name__ == "__main__":
    main()

