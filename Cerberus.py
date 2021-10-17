# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)

#TODO
# - Create classes for all applications - DONE
# - Create database for users
# - Store current users
# - User-specific notes and game progress!
# - Add more games in class format
# - Fix imports

from operating_system import OperatingSystem
from jokes import Jokes
from notepad import Notepad
from bagels import Bagels
from tictactoe import TicTacToe
from task_manager import TaskManager
from user_settings import UserSettings
from system_info import SysInfo
from reset import Reset

# Initializing all classes for apps
jokes = Jokes()
notepad = Notepad()
bagelsGame = Bagels()
tictactoeGame = TicTacToe()
taskManager = TaskManager()
userSettings = UserSettings()
systemInfo = SysInfo()
reset = Reset()

#Users and Passwords dictionary
#First try to make a new database if it doesn't exist already.
user_pwd_dictionary = {}
try:
    user_pwd_database = open('userpwd_db.txt', "x")
#If the database exists, run through the whole thing and add it to the dictionary stored in memory.
except FileExistsError:
    #Make dictionary and variables.
    user_pwd_database = open('userpwd_db.txt', "r")
    #Running through the lines of the database.
    count = 0
    for i in user_pwd_database:
        #Split the line into the three parts and append the user and password to the dictionary above.
        (user, pwd, current) = i.split('\t\t', 2)
        #If the user is specified as the current, write that in the dictionary.
        if current == 'CURRENT\n':
            user_pwd_dictionary[count] = user, pwd, current
        else:
            user_pwd_dictionary[count] = user, pwd, '\n'
        count += 1
    user_pwd_database.close()

#Initializing Notes
notes_dictionary = {}
#Same as above. Try creating the notes database and simply read it if it exists already.
try:
    notes_database = open('user_notes.txt', 'x')
except FileExistsError:
    notes_database = open('user_notes.txt', 'r')
    for i in notes_database:
        (user, notes) = i.split('\t\t', 1)
        user_notes = notes
        while '\t' in user_notes:
            (notes1, notes2) = user_notes.split('\t', 1)
            user_notes = notes1 + '\n' + notes2
        notes_dictionary[user] = user_notes
    notes_database.close()

#Versions and Stats Dictionaries.
versions = {"main": 6.6, "jokes": 1.1, "notes": 1.2, "bagels": 1.4, "tictactoe": 1.2, "userset": 1.4, "sysinfo": 1.2}
stats = {"main": "not running", "jokes": "not running", "notes": "not running", "bagels": "not running",
         "tictactoe": "not running", "userset": "not running", "sysinfo": "not running", "setup": "n"}

#Initializing operating system with __init__
args = [user_pwd_dictionary, notes_dictionary, jokes, notepad, bagelsGame, tictactoeGame, taskManager, userSettings, systemInfo, reset]
operating_system = OperatingSystem(args)

#Hard reset everything before booting up.
reset.reset(stats)

#If the user_pwd dictionary exists (meaning the database exists), run startup. Otherwise create it and go into setup.
if user_pwd_dictionary:
    operating_system.startup(versions, stats)
else:
    operating_system.setup(user_pwd_dictionary)
    operating_system.startup(versions, stats)
