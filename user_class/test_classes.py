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

import user
import user_constants
import user_saver


##########
# Tests
##########

def test_csv_headers():
    """
    Test if UserSaver.get_csv_headers() functions correctly.
    """
    jai = user.instantiate_user()
    keys = user_saver.UserSaver.get_csv_headers(jai).split(',')
    for k in keys:
        print(k)


def test_write_user_info():
    """
    Test if UserSaver writes user info correctly.
    """
    jai = user.instantiate_user()
    users = [jai]

    user_saver.UserSaver.write_users_to_csv(users)
    

##########
# Main
##########



def main():
    """
    Run module unit tests.
    """
    # test_csv_headers()
    test_write_user_info()


if __name__ == "__main__":
    main()

