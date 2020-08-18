"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-16 20:23:46
 * @modify date 2020-08-17 17:40:00
 * @desc [
    Parent user class that contains constants to reference.

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
        - API urls
        - Auxiliary lists
        - Activity modes
        - Key Tuples - dictionary data structures

    NOTE: Careful consideration of tuple data structure 
    Even if single item, must still have comma after so 
    script considers the structure iterable 
    """

    ##########
    # API URLs
    ##########

    user_url = "https://api.chess.com/pub/player/{}"
    user_stats_url = "https://api.chess.com/pub/player/{}/stats"
    

    ##########
    # Aux lists
    ##########

    timestamps_to_datetimes = (
        'joined',
        'date',
    )
    
    
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


