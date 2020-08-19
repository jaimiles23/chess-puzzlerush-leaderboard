"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-17 19:00:53
 * @modify date 2020-08-17 19:00:53
 * @desc [
    Logger.
 ]
 */
"""


##########
# Logger
##########

import logging

logger = logging.getLogger(__name__ + "user_class")
logger.setLevel(10)

"""
NOTE: 
before commenting, this worked. Check if logger comes AFTER commenting.

ALSO, create new directory for loggers to write to.

ALSO, remove that dir from gitignore.

ALSO, fix the logger format.
"""