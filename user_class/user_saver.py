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
    from user_class.create_user_class import User
    from user_class.user_constants import UserConstants

except: 
    from create_user_class import User
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

    csv_file_name = "{}/{}/{}_{}:{}:{}_puzzlerush_leaderboard.csv"


    ##########
    # CSV Methods
    ##########

    @staticmethod
    def write_users_to_csv(Users: list) -> None:
        """
        Writes passed users to csv.
        """
        csv_file_name = UserSaver.get_csv_file_name()

        with open(csv_file_name, 'w') as f:
            
            for u in Users:
                ## TODO: get values for each user.
                f.write(u)


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
        """Returns list of variables for csv headers.
        
        Uses recursive function to get csv headers.
        """

        ## Helper function
        def add_nested_keys(user_var: dict) -> str:
            """Returns combination of keys used in player object.
            
            If there are nested dictionaries, creates prefixes of nested keys
            """
            if not isinstance( var, dict):
                raise TypeError

            keys = []
            for k, v in user_var.items():
                
                if isinstance(v, (str, int, float, None)):
                    # if value, add key.
                    keys.append(k)
                
                elif isinstance(v, dict):
                    nested_keys = add_nested_keys(v)
                    prefixed_keys = ['_'.join([k, key]) for key in nested_keys]
                    keys += prefixed_keys
                
                else:
                    raise TypeError
            return keys


        ## Get csv headers
        csv_headers = list()

        for v in vars(user_obj):

            print(v, end = ' - ')
            var = getattr(user_obj, v)
            print(type(var))
            print(var)

            if isinstance( var, (str, int, float)):
                print('base')
                csv_headers.append(var)

            elif isinstance( var, dict):
                print('dict')
                csv_headers += add_nested_keys(var)

            else:
                raise TypeError
        
        return csv_headers


    ##########
    # User Methods
    ##########

    @staticmethod
    def format_user_vars_for_csv( User: object) -> list:
        """Returns list of user object attributes for csv format.

        Uses helper function get_nested_val to traverse dictionaries.
        """

        def get_nested_val(value_dict: Any) -> Union[str, int, float]:
            """Returns all values and nested values from dictionary."""
            item_values = []

            for v in value_dict.values():
                if isinstance(v, (str, int, float)):
                    item_values.append(v)
                
                elif isinstance(v, dict):
                    for k, v in v.items():
                        item_values += UserSaver.get_nested_val(v)
                
                else:
                    raise Exception(f"Unrecognized var type: {v}")
            
            return item_values


        ## Create user vars
        user_vars = list()

        for var in vars(User):
            if isinstance(var, (str, int, float)):
                user_vars.append(User.var)
            
            elif isinstance(var, dict):
                user_vars += UserSaver.get_nested_val(var)

            else:
                raise Exception(f"Unrecognized var type: {var}")

        return user_vars

    

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

