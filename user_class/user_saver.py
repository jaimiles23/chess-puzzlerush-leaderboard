"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-16 17:40:01
 * @modify date 2020-08-16 17:40:01
 * @desc [
    Class to save user profiles to csv.


    May like to
 ]
 */
"""


##########
# Imports
##########

from datetime import datetime
from typing import Union, Any

## NOTE: Could also use if name == main for import statements..?
try:
    from user_class.user import User
    from user_class.user_constants import UserConstants

except: 
    from user import User
    from user_constants import UserConstants


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

    csv_file_name = "{}.{}.{}_{}:{}:{}_puzzlerush_leaderboard.csv"


    ##########
    # CSV Methods
    ##########

    @staticmethod
    def write_users_to_csv(Users: list) -> None:
        """
        Writes passed users to csv.
        """
        csv_file_name = UserSaver.get_csv_file_name()
        csv_file_name=  'testing.csv'

        with open(csv_file_name, 'w') as f:

            for User in Users:
                user_info = UserSaver.get_user_info(User)
                f.write(user_info)
        
        return


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


    # NOTE: may like to make Union type of these to simplify.
    # base_classes = Union[str, int, float]

    @staticmethod
    def get_csv_headers( user_obj: object) -> list:
        """Returns list of variables for csv headers."""
        return vars(user_obj)


    ##########
    # User Methods
    ##########

    @staticmethod
    def get_user_info( user_obj: object) -> list:
        """Returns list of user information to write to csv."""
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
