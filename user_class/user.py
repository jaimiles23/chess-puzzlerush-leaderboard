"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-15 23:06:48
 * @modify date 2020-08-18 15:30:07
 * @desc [
    Contains player class to hold player's statistics.

    NOTE
    I process the chess.com API data into a standardized form within each user profile.
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
    from user_constants import UserConstants
    from logger import logger

except:
    from user_class.user_constants import UserConstants
    from user_class.logger import logger


##########
# Class-specific types
##########

AttrInfo = Tuple[str, Union[str, int]]  # User attr field & info to assign to attr
AttrInfoList = List[AttrInfo]

KeyTuple = Tuple[str, tuple]            # Dict key structure for API


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
    def add_user(cls, user_name: str):
        """Increments user count."""
        cls.user_count += 1
        logger.debug(f"User # {User.user_count}: {user_name}")
    

    @classmethod
    def print_num_users(cls):
        """Prints number of users."""
        print(cls.user_count)
    

    @classmethod
    def reset_num_users(cls):
        """Resets the number of users."""
        cls.user_count = 0
    

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
    

    ########## AttrInfoList
    """
    Helper methods to create AttrInfoList from user dictionaries.

    AttrInfo: (str, Union[str, int, float]). 
        AttrsInfo[0] represents the user's attribute
        AttrsInfo[1] represents the user's info
    """
    @staticmethod
    def get_attrinfolist(user_stat_dict: dict, key_tuple: KeyTuple, mode: str) -> AttrInfoList:
        """Returns list of (attr, info) from top_dict which are specified in the key_tuple.

        NOTE: Consider more flexible solutions - recursion/iteration
        """
        mode_dict = user_stat_dict.get(mode, None)
        attr_info_list = list()

        for key, nested_key_tuple in key_tuple:
            for nested_key in nested_key_tuple:
                new_key = '_'.join([mode, key, nested_key])
                
                try:
                    nested_dict = mode_dict.get(key, None)
                    value = nested_dict.get(nested_key, None)
                
                except (KeyError, AttributeError) as e:
                    value = None
                    logger.debug(f"\t{e}: {key}, {nested_key}")
                
                finally:
                    value = value if (value is not None) else ''
                    attr_info_list.append( (new_key, value))
        
        return attr_info_list


    @staticmethod
    def get_mode_attrinfolist(
        user_stat_dict: dict,
        modes: tuple, 
        key_tuple: KeyTuple
        ) -> AttrInfoList:
        """Returns user's list of AttrInfoList for each mode.

        params:
        > user_stat_dict: dict. User dict of all user statistics
        > modes: tuple. Modes to access from user_stat_dict.
        > dict_key_strucutre: tuple. Mapping of the dict keys in the mode dictionary.
        """
        attr_info_list = []
        
        for mode in modes:
            attr_info = User.get_attrinfolist(
                user_stat_dict = user_stat_dict,
                key_tuple = key_tuple, 
                mode = mode
            )
            attr_info_list.append(attr_info)
        
        return attr_info_list


    ##########
    # Initialize
    ##########

    def __init__(self, username: str, score: int):
        """Initializes user instance with username and score.

        From username, accesses chess.com API and records info on:
        - player info
        - player ratings
        - practice
        - puzzle rush
        - daily

        NOTE: information on player_id and score are set first
        because this is ultimate the information of interest.
        """

        ## First, then later set by set_attrinfo_userinfo()
        self.player_id = None

        ## Init args
        self.score = str(score)
        self.username = username
        

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

        ## Clean attrs
        self.clean_location()
        self.set_country_code()
        self.convert_timestamp_attrs()

        ## increment user
        User.add_user( self.username)

        ## clean user attr

        ## clean attr
        self.__delattr__('user_info_dict')
        self.__delattr__('user_stats_dict')


    ##########
    # User API info
    ##########

    def fetch_userinfo_dict(self) -> dict:
        """Returns dict from user's chess.com API"""
        return User.get_chessAPI_json( self.user_url)
    

    def fetch_userstats_dict(self) -> dict:
        """Returns dict from user's chess.com stats API"""
        return User.get_chessAPI_json( self.user_stats_url)


    ##########
    # AttrInfo methods
    ##########

    ########## Set AttrInfo Helper methods
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


    ########## User Info
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
            value = value if (value is not None) else ''
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


    ##########
    # Clean attr methods
    ##########

    ########## Location
    def clean_location(self) -> None:
        """Removes commas from User.location attribute and encodes in utf8.

        If there are commas, displaces csv format.
        e.g., La Jolla, California.

        Not all locations are in ascii range(128). Thus, encode into utf8
        """
        self.location = self.location.replace(',', '')
        return


    ########## Datetime
    def convert_timestamp_attrs(self) -> None:
        """Converts timestamp data to str dates.

            - joined attr
            - any attr with 'date' in the name.
        """

        def _get_datetime_str(timestamp: int) -> str:
            """Auxiliary method to return datetime string from timestamp."""
            if not timestamp:         # attrInfo records as string to record to CSV.
                return timestamp
            
            datetime_obj = datetime.fromtimestamp( int(timestamp))
            return datetime_obj.strftime("%Y/%m/%d")


        ## Convert joined
        joined_timestamp = getattr(self, 'joined')
        setattr(self, 'joined', _get_datetime_str(joined_timestamp))

        ## Convert attr with date in name.
        for attr in vars(self):
            if 'date' in attr:
                attr_timestamp = getattr(self, attr)
                setattr(self, attr,
                    _get_datetime_str(attr_timestamp))
        return


    ########## Country
    def set_country_code(self) -> None:
        """Sets player's country attr to code represented by 2-character ISO 3166 code.
        
        ISO 3166 code:
        https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

        Chess.com API format:
        https://api.chess.com/pub/country/{iso}

        NOTE: 
            - Can compare country tzs in data analysis.
        """
        url_base = "https://api.chess.com/pub/country/"
        country_attr = getattr(self, 'country')

        ## Test country attr
        assert len( country_attr) == len(url_base) + 2
        assert country_attr.find(url_base) != -1

        setattr(self, 'country', country_attr[-2:])
        return
    

    ##########
    # View profile 
    ##########

    def view_profile(self, full: bool = False) -> None:
        """Prints attributes from the player profile for viewing."""
        if full:
            for v in vars(self):
                print(v, '-', getattr(self, v))

        else:
            attr_list = [
                "username",
                "score",
                "country"
            ]
            attr_val_list = [getattr(self, attr) for attr in attr_list]
            print(attr_val_list, sep = " - ")
        
        print("\n")


##########
# Main
##########

def instantiate_user():
    # username = "jaimiles23"
    username = "kawaiikoto"
    """
    kawaiikoto has no lessons, rapid, or bullet stats.
    """
    score = 23

    test_user = User(username, score)
    return test_user


def test_user_class(jai):

    jai.view_profile(full = True)
    return


def main():
    jai = instantiate_user()
    test_user_class(jai)


if __name__ == "__main__":
    main()

