# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)

from operating_system import OperatingSystem
from User import StandardUser, Administrator
from bagels import Bagels
from tictactoe import TicTacToe
from hangman import Hangman

protected_db_name = 'db_protected.txt'
unprotected_db_name = 'db_unprotected.txt'
section1 = ""
section2 = ""
section3 = ""
section4 = ""
corrupt_message = "\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nTHE DATABASE IS CORRUPTED. PLEASE CHECK THE MANUAL, QUIT THE OS, AND RECONFIGURE THE DATABASE." \
                  "\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nCorrupted Database: %s\nCorrupted Section: %s\n"
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
    # noinspection PyTypeChecker
    for i in protected_db:
        # Split the line into the three parts and append the user and password to the dictionary above.
        progress = "0"
        try:
            (userType, rest) = i.split('\t\t', 1)
            for j in range(1, 5):
                progress = str(j)
                (globals()["section" + str(j)], rest) = rest.split('\t\t', 1)
                pass
        except ValueError:
            print(corrupt_message % ("db_protected.txt", progress))
            break
        # If the user is specified as the current, write that in the dictionary.
        while '\t' in section4:
            (notes1, notes2) = section4.split('\t', 1)
            section4 = notes1 + '\n' + notes2
        users.append(globals()[userType](section1, section2, section3 == "True", section4))
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
    count = 0
    # noinspection PyTypeChecker
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
            print(corrupt_message % ("db_unprotected", progress))
            break

        # Read TTT progress into memory.
        try:
            (board, turn, letter) = section1.split('.', 2)
            # Translation algorithm to convert the board from a comma-separated string into a list.
            while ',' in board:
                (board1, board2) = board.split(',', 1)
                board = board1 + board2
            ttt_board = []
            for j in range(len(board)):
                ttt_board.append(board[j])
            users[count].ttt = TicTacToe(user, ttt_board, turn, letter)
            pass
        except ValueError:
            print(corrupt_message + "T\n")
            break

        # Read Bagels progress into memory.
        try:
            (last_guess, num_guesses, num_digits, secret_num, max_guesses) = section2.split('.', 4)
            users[count].bagels = Bagels(user, section2.split('.', 4)[0], section2.split('.', 4)[1], section2.split('.', 4)[2], section2.split('.', 4)[3], section2.split('.', 4)[4])
            pass
        except ValueError:
            print(corrupt_message + "B\n")
            break

        try:
            users[count].hangman = Hangman(user, section3.split('.', 3)[0], section3.split('.', 3)[1], section3.split('.', 3)[2], section3.split('.', 3)[3])
            pass
        except ValueError:
            print(corrupt_message + "H\n")
            break

        # Read the stats into memory.
        users[count].saved_state = {"Jokes": section4.split('.', 7)[0], "Notepad": section4.split('.', 7)[1], "Bagels Game": section4.split('.', 7)[2],
                                    "TicTacToe": section4.split('.', 7)[3], "Hangman": section4.split('.', 7)[4], "User Settings": section4.split('.', 7)[5],
                                    "System Info": section4.split('.', 7)[6]}
        count += 1
        pass
    if flag:
        # What happens when there is no progress at all?
        for i in users:
            i.bagels = Bagels(i.username, ' ', ' ', ' ', ' ', ' ')
            i.ttt = TicTacToe(i.username, [' '] * 9, 0, ' ')
            i.hangman = Hangman(i.username, ' ', ' ', ' ', ' ')
            i.saved_state = {"Jokes": "not running", "Notepad": "not running", "Bagels Game": "not running",
                             "TicTacToe": "not running", "Hangman": "not running", "User Settings": "not running",
                             "System Info": "not running"}
        pass
    unprotected_db.close()

# Versions and Stats Dictionaries.

# Initializing operating system with __init__
Cerberus = OperatingSystem(users)

# If the user_pwd dictionary exists (meaning the database exists), run startup. Otherwise create it and go into setup.
if len(users) <= 0:
    Cerberus.startup()
    pass
while True:
    if Cerberus.startup() == 'restart':
        pass
    else:
        break
