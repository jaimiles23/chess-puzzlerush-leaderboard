"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-16 17:40:01
 * @modify date 2020-08-17 18:24:40
 * @desc [
    Class to save user profiles to csv.
 ]
 */
"""


##########
# Imports
##########

import os


from datetime import datetime
from typing import Union, Any


## NOTE: Could also use if name == main for import statements..?
try:
    from user_class.user import User
    from user_class.user_constants import UserConstants
    from user_class.logger import logger

except: 
    from user import User
    from user_constants import UserConstants
    from logger import logger


##########
# UserSaver class
##########

class UserSaver(UserConstants):
    """
    Class with auxiliary methods to save user profiles.
    """

    ##########
    # Class Constants
    ##########

    directory = "puzzlerush_csvs"
    csv_file_name = directory + "\\{}.{}.{}_{}.{}.{}_puzzlerush_leaderboard.csv"


    ##########
    # Write to CSV
    ##########

    @staticmethod
    def write_users_to_csv(Users: list) -> None:
        """
        Writes passed users to csv.
        """
        UserSaver.mkdir_if_needed()
        csv_file_name = UserSaver.get_csv_file_name()
        logger.debug(f"{'#' * 5} Logging to: {csv_file_name}")

        with open(csv_file_name, 'w') as f:
            ## CSV Headers
            csv_headers = UserSaver.get_csv_headers( Users[0])
            f.write(csv_headers)
            f.write('\n')

            ## User Info
            for User in Users:
                logger.debug(f"User: {User.username}")
                user_info = UserSaver.get_user_info(User)
                
                print(user_info)
                f.write(user_info)
                f.write('\n')
        
        logger.info(f"{'#' * 5} Logged users to: {csv_file_name}")
        return


    ##########
    # Directory methods
    ##########
    @staticmethod
    def mkdir_if_needed() -> None:
        """If directory does not exist, then create directory.
        """
        if not os.path.exists(UserSaver.directory):
            os.makedirs(UserSaver.directory)
        return
    

    ##########
    # CSV Methods
    ##########

    @staticmethod
    def get_csv_file_name() -> str:
        """Returns name for csv file.
        
        NOTE: need to format digits HH, MM, SS
        """
        now_obj = datetime.now()
                
        return UserSaver.csv_file_name.format(
            now_obj.year,
            now_obj.month,
            now_obj.day,
            now_obj.hour,
            now_obj.minute,
            now_obj.second
        )


    @staticmethod
    def get_csv_headers( user_obj: object) -> str:
        """Returns str of variables for csv headers."""
        return ','.join(vars(user_obj))


    ##########
    # User Methods
    ##########

    @staticmethod
    def get_user_info( user_obj: object) -> str:
        """Returns str of user information to write to csv."""
        user_info = list()

        for var in vars(user_obj):
            user_info.append( getattr(user_obj, var))

        return ','.join(user_info)



##########
# Main
##########

def test_csv_name():
    """Unit tests for creating csv name"""
    file_name = UserSaver.get_csv_file_name()
    print(file_name)


def main():
    test_csv_name()


if __name__ == "__main__":
    main()

