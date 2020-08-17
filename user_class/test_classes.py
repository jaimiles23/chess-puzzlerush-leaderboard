"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-17 15:58:59
 * @modify date 2020-08-17 16:06:50
 * @desc [
    Script to test User class instantiations.

 ]
 */
"""


##########
# Imports
##########

from user_constants import UserConstants
from create_user_class import (
    User, 
    test_user_class, 
    instantiate_user
)
from user_saver_class import (
    UserSaver,
    test_csv_name,
    
)


##########
# Tests
##########

def test_csv_headers():
    """
    Test if UserSaver.get_csv_headers() functions correctly.
    """
    jai = instantiate_user()
    keys = UserSaver.get_csv_headers(jai)
    print(keys)



##########
# Main
##########





def main():
    test_csv_headers()


if __name__ == "__main__":
    main()

