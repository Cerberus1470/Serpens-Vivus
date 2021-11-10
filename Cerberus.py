# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)

# TODO
# - Loops in user settings (delete more than one user) - DONE
# - Edit username and password! - DONE
# - User-specific notes and game progress! - In progress (Notes done, games coming in...)
# - Add more games in class format
# - Fix imports - DONE
# - Add shutdown, hibernate, and sleep options on shutdown menu
# - Add user-specific app status (app sessions)
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

# Initializing Notes
notes_dictionary = {}
# Initializing Bagels Game Progress
bagels_dictionary = {}
# Initializing TTT Game Progress
ttt_dictionary = {}
# Same as above. Try creating the notes database and simply read it if it exists already.
try:
    game_prog_database = open('user_notes.txt', 'x')
except FileExistsError:
    game_prog_database = open('user_notes.txt', 'r')
    for i in game_prog_database:
        (user, notes, new_line) = i.split('\t\t', 4)
        user_notes = notes
        while '!' in user_notes:
            (notes1, notes2) = user_notes.split('!', 1)
            user_notes = notes1 + '\n' + notes2
        notes_dictionary[user] = user_notes
    game_prog_database.close()
    pass

# Reading from saved_state database!
saved_state = {}
try:
    saved_state_database = open('saved_state.txt', 'x')
except FileExistsError:
    saved_state_database = open('saved_state.txt', 'r')
    for i in saved_state_database:
        (user, stats, bagels, ttt, new_line) = i.split('\t\t', 4)
        saved_state[user] = {"Jokes": stats.split('.', 6)[0], "Notepad": stats.split('.', 6)[1], "Bagels Game": stats.split('.', 6)[2],
                             "TicTacToe": stats.split('.', 6)[3], "User Settings": stats.split('.', 6)[4], "System Info": stats.split('.', 6)[5]}
        user_ttt = ttt
        (board, turn, letter) = user_ttt.split('.', 2)
        ttt_board = []
        while ',' in board:
            (board1, board2) = board.split(',', 1)
            board = board1 + board2
        for j in range(len(board)):
            ttt_board.append(board[j])
        ttt_dictionary[user] = ttt_board, turn, letter
        (last_guess, num_guesses, num_digits, secret_num, max_guesses) = bagels.split('.', 4)
        bagels_dictionary[user] = last_guess, num_guesses, num_digits, secret_num, max_guesses

# Versions and Stats Dictionaries.
versions = {"main": 6.6, "jokes": 1.1, "notes": 1.2, "bagels": 1.4, "tictactoe": 1.2, "userset": 1.4, "sysinfo": 1.2}

# Initializing operating system with __init__
args = [user_pwd_dictionary, notes_dictionary, bagels_dictionary, ttt_dictionary, saved_state]
operating_system = OperatingSystem(args)

# If the user_pwd dictionary exists (meaning the database exists), run startup. Otherwise create it and go into setup.
if user_pwd_dictionary:
    operating_system.startup(versions)
else:
    operating_system.setup(user_pwd_dictionary)
    operating_system.startup(versions)
