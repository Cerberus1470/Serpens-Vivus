# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)

from operating_system import OperatingSystem
from User import User
from bagels import Bagels
from tictactoe import TicTacToe
from hangman import Hangman

protected_db_name = 'db_protected.txt'
unprotected_db_name = 'db_unprotected.txt'
corrupt_message = "\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nTHE DATABASE IS CORRUPTED. PLEASE CHECK THE MANUAL, QUIT THE OS, AND RECONFIGURE THE DATABASE."
"\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nCorrupted Database: db_protected.txt\nCorrupted Section: "
user_pwd_dictionary = {}
users = []
# Users and Passwords dictionary
# First try to make a new database if it doesn't exist already.
try:
    protected_db = open(protected_db_name, "x")
# If the database exists, run through the whole thing and add it to the dictionary stored in memory.
except FileExistsError:
    # Make dictionary and variables.
    protected_db = open(protected_db_name, "r")
    # Running through the lines of the database.
    for i in protected_db:
        # Split the line into the three parts and append the user and password to the dictionary above.
        progress = "0"
        try:
            (user, rest) = i.split('\t\t', 1)
            for j in range(1, 3):
                progress = str(j)
                (globals()["section" + str(j)], rest) = rest.split('\t\t', 1)
                pass
        except ValueError:
            print(corrupt_message + progress + "\n")
            break
        # If the user is specified as the current, write that in the dictionary.
        while '!' in rest:
            (notes1, notes2) = rest.split('!', 1)
            rest = notes1 + '\n' + notes2
        if section2 == 'CURRENT':
            users.append(User(user, section1, section2, rest))
        else:
            users.append(User(user, section1, '\n', rest))
    protected_db.close()
    pass

# Reading from saved_state database!
saved_state = []
# Initializing Bagels Game Progress
bagels = []
# Initializing TTT Game Progress
ttt = []
# Initializing Hangman Game Progress
hangman = []
# Try creating the save state, and read it if it exists.
try:
    unprotected_db = open(unprotected_db_name, 'x')
except FileExistsError:
    unprotected_db = open(unprotected_db_name, 'r')
    # Reading from the file.
    flag = True
    for i in unprotected_db:
        # Split the line into each data set.
        flag = False
        progress = 0
        try:
            (user, rest) = i.split('\t\t', 1)
            for j in range(1, 5):
                progress = str(j)
                (globals()["section" + str(j)], rest) = rest.split('\t\t', 1)
        except ValueError:
            print(corrupt_message + progress + "\n")
            break
        # Read the stats into memory.
        saved_state[user] = {"Jokes": section1.split('.', 7)[0], "Notepad": section1.split('.', 7)[1], "Bagels Game": section1.split('.', 7)[2],
                             "TicTacToe": section1.split('.', 7)[3], "Hangman": section1.split('.', 7)[4], "User Settings": section1.split('.', 7)[5],
                             "System Info": section1.split('.', 7)[6]}

        # Read Bagels progress into memory.
        try:
            (last_guess, num_guesses, num_digits, secret_num, max_guesses) = section2.split('.', 4)
            bagels.append(Bagels(user, last_guess, num_guesses, num_digits, secret_num, max_guesses))
            bagels[user] = section2.split('.', 4)
            pass
        except ValueError:
            print(corrupt_message + "B\n")
            break

        # Read TTT progress into memory.
        try:
            (board, turn, letter) = section3.split('.', 2)
            # Translation algorithm to convert the board from a comma-separated string into a list.
            while ',' in board:
                (board1, board2) = board.split(',', 1)
                board = board1 + board2
            ttt_board = []
            for j in range(len(board)):
                ttt_board.append(board[j])
            ttt.append(TicTacToe(user, ttt_board, turn, letter))
            pass
        except ValueError:
            print(corrupt_message + "T\n")
            break
        try:
            (correct_letters, missed_letters, secret_key, secret_word) = section4.split('.', 3)
            hangman.append(Hangman(user, correct_letters, missed_letters, secret_key, secret_word))
            pass
        except ValueError:
            print(corrupt_message + "H\n")
            break
        unprotected_db.close()
        pass
    if flag:
        # What happens when there is no progress at all?
        for i in users:
            bagels.append(Bagels(i.username, ' ', ' ', ' ', ' ', ' '))
            ttt.append(TicTacToe(i.username, [' '] * 9, 0, ' '))
            hangman.append(Hangman(i.username, ' ', ' ', ' ', ' '))
            saved_state.append({"Jokes": "not running", "Notepad": "not running", "Bagels Game": "not running",
                                "TicTacToe": "not running", "Hangman": "not running", "User Settings": "not running",
                                "System Info": "not running"})
        pass
    for i in range(len(users)):
        users[i].__setGames__(bagels[i], ttt[i], hangman[i], saved_state[i])

# Versions and Stats Dictionaries.

# Initializing operating system with __init__
operating_system = OperatingSystem(users)

# If the user_pwd dictionary exists (meaning the database exists), run startup. Otherwise create it and go into setup.
if len(users) > 0:
    while True:
        if operating_system.startup() == 'restart':
            break
        else:
            pass
else:
    operating_system.setup(user_pwd_dictionary)
    while True:
        if operating_system.startup() == 'restart':
            break
        else:
            pass
