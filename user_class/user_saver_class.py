"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-16 17:40:01
 * @modify date 2020-08-16 17:40:01
 * @desc [
    Class to save user profiles to csv.
 ]
 */
"""


##########
# Imports
##########

from datetime import datetime
from typing import Union

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

   ##########
   # Class Constants
   ##########

   csv_file_name = "{}/{}/{}_{}:{}:{}_puzzlerush_leaderboard.csv"

   """
   Class with auxiliary methods to save user profile.
   """

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
      """Returns name for csv file."""

      now_obj = datetime.now()
      return UserSaver.csv_file_name.format(
         now_obj.year,
         now_obj.month,
         now_obj.day,
         now_obj.hour,
         now_obj.minute,
         now_obj.second
      )


   ##########
   # User Methods
   ##########

   @staticmethod
   def format_user_vars_for_csv( User: object) -> list:
      """Returns list of user object attributes for csv format.

      NOTE: Want to somehow place user ID at front of list.
      """
      user_attr = list()

      user_attr += UserSaver.get_user_info(User)

      user_attr.insert(1, User.username)
      user_attr.insert(2, User.score)

      ## ratings

      ## practices

      ## puzzlerush




      return user_attr


   @staticmethod
   def get_user_info( User: object) -> list:
      """Returns list of user info.
      
      NOTE: player_id is first constant in list.
      """
      user_info = []

      for key in UserSaver.keys_info:
         value = User.user_info[key]
         user_info.append(value)
      
      return user_info
   

   @staticmethod
   def get_all_user_stats( user_stats_dict: dict) -> list:
      """Returns list of user stats for different game ratings.

      Uses recursive helper function to get all dictionary keys and values
      """

      def get_dict_values( nested_dict: dict) -> Union[str, int]:
         """Recursive helper function to get nested dict values."""
         if type(nested_dict) != dict:
            return nested_dict
         
         dict_key = []         
         for k, v in nested_dict.items():
            



      user_stat_ratings = []
      # NOTE: Could create recursive structure instead?

      for k, v in user_stats_dict:

         if type(v) == dict:
            pass
      
      return user_stat_ratings


##########
# Main
##########

def main():
   pass


if __name__ == "__main__":
   main()

