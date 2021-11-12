# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)

# TODO
# - Loops in user settings (delete more than one user) - DONE
# - Edit username and password! - DONE
# - User-specific notes and game progress! - DONE
# - Add more games in class format
# - Fix add user with game progress
# - Merge shutdown and hibernate (since they share a lot of root code)
# - Fix imports - DONE
# - Add shutdown, hibernate, and sleep options on shutdown menu - DONE
# - Add user-specific app status (app sessions) - DONE
# - Change status dictionary - DONE

from operating_system import OperatingSystem

# Users and Passwords dictionary
# First try to make a new database if it doesn't exist already.
user_pwd_dictionary = {}
try:
    user_pwd_database = open('userpwd_db.txt', "x")
# If the database exists, run through the whole thing and add it to the dictionary stored in memory.
except FileExistsError:
    # Make dictionary and variables.
    user_pwd_database = open('userpwd_db.txt', "r")
    # Running through the lines of the database.
    for i in user_pwd_database:
        # Split the line into the three parts and append the user and password to the dictionary above.
        (user, pwd, current) = i.split('\t\t', 2)
        # If the user is specified as the current, write that in the dictionary.
        if current == 'CURRENT\n':
            user_pwd_dictionary[user] = pwd, current
        else:
            user_pwd_dictionary[user] = pwd, '\n'
    user_pwd_database.close()
    pass

# Initializing Notes
notes_dictionary = {}
# Try creating the notes database and simply read it if it exists already.
try:
    game_prog_database = open('user_notes.txt', 'x')
except FileExistsError:
    game_prog_database = open('user_notes.txt', 'r')
    for i in game_prog_database:
        (user, notes, new_line) = i.split('\t\t', 2)
        user_notes = notes
        while '!' in user_notes:
            (notes1, notes2) = user_notes.split('!', 1)
            user_notes = notes1 + '\n' + notes2
        notes_dictionary[user] = user_notes
    game_prog_database.close()
    pass

# Reading from saved_state database!
saved_state = {}
# Initializing Bagels Game Progress
bagels_dictionary = {}
# Initializing TTT Game Progress
ttt_dictionary = {}
# Initializing Hangman Game Progress
hangman_dictionary = {}
# Try creating the save state, and read it if it exists.
try:
    saved_state_database = open('saved_state.txt', 'x')
except FileExistsError:
    saved_state_database = open('saved_state.txt', 'r')
    # Reading from the file.
    for i in saved_state_database:
        # Split the line into each data set.
        (user, stats, bagels, ttt, hangman, new_line) = i.split('\t\t', 5)
        # Read the stats into memory.
        saved_state[user] = {"Jokes": stats.split('.', 7)[0], "Notepad": stats.split('.', 7)[1], "Bagels Game": stats.split('.', 7)[2],
                             "TicTacToe": stats.split('.', 7)[3], "Hangman": stats.split('.', 7)[4], "User Settings": stats.split('.', 7)[5],
                             "System Info": stats.split('.', 7)[6]}
        # Read TTT progress into memory.
        (board, turn, letter) = ttt.split('.', 2)
        ttt_board = []
        # Translation algorithm to convert the board from a comma-separated string into a list.
        while ',' in board:
            (board1, board2) = board.split(',', 1)
            board = board1 + board2
        for j in range(len(board)):
            ttt_board.append(board[j])
        ttt_dictionary[user] = ttt_board, turn, letter
        # Read Bagels and Hangman progress into memory.
        bagels_dictionary[user] = bagels.split('.', 4)
        hangman_dictionary[user] = hangman.split('.', 3)
    saved_state_database.close()
    pass

# Versions and Stats Dictionaries.
# Remove a space after a comma to reformat the file.
versions = {"main": 8.0, "jokes": 1.2, "notes": 1.3, "bagels": 1.7, "tictactoe": 1.5, "hangman": 1.2, "userset": 1.5, "sysinfo": 1.3}

# Initializing operating system with __init__
args = [user_pwd_dictionary, notes_dictionary, bagels_dictionary, ttt_dictionary, hangman_dictionary, saved_state]
operating_system = OperatingSystem(args)

# If the user_pwd dictionary exists (meaning the database exists), run startup. Otherwise create it and go into setup.
if user_pwd_dictionary:
    operating_system.startup(versions)
else:
    operating_system.setup(user_pwd_dictionary)
    operating_system.startup(versions)
