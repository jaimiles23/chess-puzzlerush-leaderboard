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

from user_class.create_user_class import User
from user_class.user_constants import UserConstants


##########
# UserSaver class
##########

class UserSaver(UserConstants):
   """
   Class with auxiliary methods to save user profile.
   """

   @staticmethod
   def format_user_attr_for_csv( User: object) -> list:
      """Returns list of user object attributes for csv format.

      NOTE: Want to somehow place user ID at front of list.
      """
      user_attr = list()

      user_attr += UserSaver.get_user_info(User)

      ## insert @ index1&2, username & score



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



    
