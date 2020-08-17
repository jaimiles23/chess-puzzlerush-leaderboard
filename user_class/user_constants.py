"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-16 20:23:46
 * @modify date 2020-08-16 20:23:46
 * @desc [
    Parent user class that contains constants used for

 ]
 */
"""


##########
# Imports
##########



##########
# UserConstants
##########

class UserConstants(object):
    """
    Parent class that contains constants for:
        - Activity modes
        - Dictionary data structures

    NOTE: Careful consideration of tuple data structure 
    Even if single item, must still have comma after so 
    script considers the structure iterable 
    """

    ##########
    # Modes
    ##########

    modes_play = (
        "chess_blitz",
        "chess_bullet",
        "chess_daily",
        "chess_rapid",
    )
    modes_practice = (
        "tactics",
        "lessons",
    )
    modes_puzzle_rush = (
        "puzzle_rush",
    )


    ##########
    # Data structures
    ##########
    """
    Tuple data structures holding dict keys to acccess user info from chess.com API.

    keys_info:
        - account info
    keys_games:
        - chess_blitz
        - chess_bullet
        - chess_daily
        - chess_rapid
    keys_practice:
        - tactics
        - lessons
    keys_puzzlerush:
        - puzzle rush
    keys_daily:
        - daily puzzles
    """

    keys_info = (
        'player_id',
        'username', 
        'country',
        'location', 
        'joined',
        'status',
        "is_streamer",
    )
    keys_games = (
        ( "last", 
            ("rating", "date")),
        ("best", 
            ("rating", "date")),
        ("record",
            ("win", "loss", "draw"))
    )
    keys_practice = (
        ("highest", 
            ("rating", "date")),
    )
    keys_puzzlerush = (
        ("best",
            ("total_attempts", "score")),
        ("daily", 
            ("total_attempts", "score"))
    )
    """
    NOTE
    Puzzle rush daily stats are not available if user has not yet played today.
    Because users are scraped from puzzlerush scoreboard, this should not present an issue.
    """


