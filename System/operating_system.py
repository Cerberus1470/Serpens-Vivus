import os
from System import Loading
from System import User
from System.task_manager import TaskManager
from System.reset import Reset
from System.event_viewer import EventViewer
from Applications.bagels import Bagels
from Applications.hangman import Hangman
from Applications.jokes import Jokes
from Applications.notepad import Notepad
from Applications.system_info import SystemInfo
from Applications.tictactoe import TicTacToe
from Applications.user_settings import UserSettings
from Applications.speed_up_or_slow_down import SpeedSlow
import traceback


# noinspection PyBroadException
def boot():
    running = True
    while running:
        try:
            # Initialization reads all files and data from disk and loads it into memory.
            Loading.log("System Startup")
            cerberus = OperatingSystem()
            # Logic to run setup
            if len(cerberus.users) <= 0:
                cerberus.setup()
            # Logic for restarting.
            if cerberus.startup() == 4:
                Loading.returning("Restarting system...", 2)
                Loading.returning("Booting...", 2)
                pass
            else:
                running = False
        # Screen for fatal errors. Catches all exceptions and prints the stacktrace. Allows for a reboot.
        except Exception:
            for i in range(20):
                print("\n")
            Loading.log("!!! The system encountered a fatal error. Reboot is required. !!!")
            if input('!!! The system encountered a fatal error. Reboot is required. !!! \nStacktrace: ' + str(traceback.format_exc()) + '\nType "REBOOT" to reboot.') == "REBOOT":
                pass
            else:
                print("Goodbye")
                running = False
        Loading.log("System Shutdown.")


# noinspection PyTypeChecker
class OperatingSystem:

    def __init__(self):
        # User list, name, and versions. All inherent settings.
        self.users = []
        self.name = "Cerberus"
        self.utilities = ["User Settings", "System Info\t", "Notepad\t\t", "SpeedSlow\t", "Power"]
        self.games = ["Bagels\t", "TicTacToe", "Hangman ", "Joke Teller", '\t\t']
        self.admin = ["Reset\t\t", "Event Viewer\t", "Task Manager", '\t\t', '\t\t']
        self.versions = {"Main": 5.0, "Joke Teller": 1.3, "Notepad": 3.2, "Bagels": 3.5, "TicTacToe": 4.7, "Hangman": 2.5, "Sonar": 1.0, "User Settings": 2.7, "System Info": 1.5, "Event Viewer": 1.0}
        self.user_settings = UserSettings()
        self.notepad = Notepad()
        corrupt_message = "\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nTHE DATABASE IS CORRUPTED. PLEASE CHECK THE MANUAL, QUIT THE OS, AND RECONFIGURE THE DATABASE." \
                          "\n!!!\t\t!!!\t\t!!!\t\t!!!\t\t!!!\nCorrupted Database: {}\nCorrupted Section: {}\n"

        # The main boot sequence.
        # Start by trying to create the protected database.

        unprotected_db_name = 'db_unprotected.txt'
        try:
            # Trying to make a User folder
            os.mkdir('Users')
        # If the folder exists, read from it!
        except FileExistsError:
            # Ready lines of decrypted user info.
            lines = []
            Loading.log("Reading info from memory...")
            # Looping through the User folders to read their info files.
            for subdir, dirs, files in os.walk('Users'):
                for dir1 in dirs:
                    try:
                        # The first of many user files...
                        file = open("Users\\{}\\info.usr".format(dir1), 'r')
                        lines.append(Loading.caesar_decrypt(list(file)[0].split('\n')[0]))
                        file.close()
                    except FileNotFoundError:
                        continue
            Loading.log("Decryption complete.")
            for i in lines:
                # Ready the sections!
                sections = ['USER TYPE', 'USERNAME', 'PASSWORD', 'CURRENT STATUS']
                progress = 0
                user_info = ['', '', '', '']
                try:
                    # First save the user type. (Standard vs Admin)
                    (user_info[0], rest) = i.split('\t\t', 1)
                    # Now loop for 4 more blocks, tracking progress so the user is alerted about corruption.
                    for j in range(1, 4):
                        progress = j
                        (user_info[j], rest) = rest.split('\t\t', 1)
                        pass
                except ValueError:
                    # If something is missing, print out the last stored progress to show the user that something is wrong.
                    print(corrupt_message.format("db_protected.txt", sections[progress].lower()))
                    Loading.log("The protected database is corrupted at the " + sections[progress] + " section.")
                    user_info[progress] = 'INVALID'
                if user_info[0] == 'StandardUser':
                    self.users.append(User.StandardUser(user_info[1], user_info[2], user_info[3] == "True"))
                else:
                    self.users.append(User.Administrator(user_info[1], user_info[2], user_info[3] == "True"))
            Loading.log("The protected database is finished.")
            # Setting the current user object.
            for j in range(len(self.users)):
                if self.users[j].current:
                    self.current_user = self.users[j]
                    break
            pass
        # Now for the unprotected database, also soon to be phased out.
        try:
            # Try making the unprotected db file.
            unprotected_db = open(unprotected_db_name, 'x')
            unprotected_db.close()
        except FileExistsError:
            # If the file exists, read from it!
            unprotected_db = open(unprotected_db_name, 'r')
            # A simple flag to see if the data exists, and a count to append progress to the user list.
            data = False
            count = 0
            # noinspection PyTypeChecker
            for i in unprotected_db:
                # If a line exists, the data is there. Set the flag to True.
                data = True
                # Ready the error correction!
                sections = ['USERNAME', 'TICTACTOE', 'BAGELS', 'HANGMAN', 'SAVED STATE']
                progress = 0
                game_info = ['', '', '', '']
                try:
                    # Start splitting. Get the username first.
                    (user, rest) = i.split('\t\t', 1)
                    # Then run the for loop!
                    for j in range(1, 5):
                        progress = str(j)
                        (game_info[j - 1], rest) = rest.split('\t\t', 1)
                except ValueError:
                    # Let the user know something is wrong.
                    print(corrupt_message.format("db_unprotected.txt", progress))
                    Loading.log("The unprotected database is corrupted at the " + sections[progress - 1] + " section.")
                    break

                # TTT First.
                try:
                    (board, turn, letter) = game_info[0].split('.', 2)
                    # Translation algorithm to convert the board from a comma-separated string into a list.
                    while ',' in board:
                        (board1, board2) = board.split(',', 1)
                        board = board1 + board2
                    ttt_board = []
                    for j in range(len(board)):
                        ttt_board.append(board[j])
                    # self.users[count].ttt = TicTacToe(user, ttt_board, turn, letter)
                    pass
                except ValueError:
                    # Let the user know something is wrong.
                    print(corrupt_message.format("db_unprotected.txt", "T"))
                    Loading.log("The unprotected database is corrupted at the " + sections[1] + " section.")
                    break

                # Read Bagels progress into memory.
                try:
                    self.users[count].bagels = Bagels(user, game_info[1].split('.', 4)[0], game_info[1].split('.', 4)[1], game_info[1].split('.', 4)[2], game_info[1].split('.', 4)[3], game_info[1].split('.', 4)[4])
                    pass
                except ValueError:
                    print(corrupt_message.format("db_unprotected.txt", "B"))
                    Loading.log("The unprotected database is corrupted at the " + sections[2] + " section.")
                    break

                # Read Hangman progress into memory.
                try:
                    self.users[count].hangman = Hangman(user, game_info[2].split('.', 3)[0], game_info[2].split('.', 3)[1], game_info[2].split('.', 3)[2], game_info[2].split('.', 3)[3])
                    pass
                except ValueError:
                    print(corrupt_message.format("db_unprotected.txt", "H"))
                    Loading.log("The unprotected database is corrupted at the " + sections[3] + " section.")
                    break

                # Read the open programs into memory.
                try:
                    self.users[count].saved_state = {"Jokes": game_info[3].split('.', 7)[0], "Notepad": game_info[3].split('.', 7)[1], "Bagels Game": game_info[3].split('.', 7)[2],
                                                     "TicTacToe": game_info[3].split('.', 7)[3], "Hangman": game_info[3].split('.', 7)[4], "User Settings": game_info[3].split('.', 7)[5],
                                                     "System Info": game_info[3].split('.', 7)[6]}
                except ValueError:
                    print(corrupt_message.format("db_unprotected.txt", "S"))
                    Loading.log("The unprotected database is corrupted at the " + sections[4] + " section.")
                count += 1
                pass
            Loading.log("The unprotected database is finished.")
            if not data:
                # What happens when there is no progress at all?
                Loading.log("No progress present in unprotected_db.txt. Assigning empty progress.")
                for i in self.users:
                    i.bagels = Bagels(i.username, ' ', ' ', ' ', ' ', ' ')
                    # i.ttt = TicTacToe(i.username, [' '] * 9, 0, ' ')
                    i.hangman = Hangman(i.username, ' ', ' ', ' ', ' ')
                    i.saved_state = {"Jokes": "not running", "Notepad": "not running", "SpeedSlow": "not running", "Bagels Game": "not running",
                                     "TicTacToe": "not running", "Hangman": "not running", "User Settings": "not running",
                                     "System Info": "not running"}
                pass
            unprotected_db.close()
        Loading.log("Boot complete.")
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.name + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
               self.current_user.username + "\n Current Password is hidden. >"

    def startup(self):
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
            Loading.log("System Startup.")
            # Label(main_window, text="Hello! I am Cerberus, running user: " + self.current_user + ". Type 'switch' to switch users or \"shutdown\" to shut down the system.").grid(row=0, column=0)
            print("\nHello! I am {}.".format(self.name))
            if self.current_user.username != 'Guest':
                # Separate while loop for users. Guest users head down.
                incorrect_pwd = 0
                while True:
                    if incorrect_pwd >= 3:
                        Loading.returning("You have incorrectly entered the password 3 times. The computer will now restart.", 5)
                        return 4
                    print("\nCurrent user: " + self.current_user.username + ". Type \"switch\" to switch users or \"power\" to shut down the system.")
                    # Ask for password
                    pwd = input("Enter password.\n")
                    if pwd == self.current_user.password:
                        Loading.returning("Welcome!", 1)
                        # Move to the system screen.
                        os_rv = self.operating_system()
                        Loading.log("Code {} returned. Executing task.".format(os_rv))
                        # Logic for returning from the OS screen.
                        if os_rv == 1:
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        elif os_rv == 'regular':
                            pass
                        else:
                            return os_rv
                    elif pwd == 'switch':
                        # Switch users!
                        self.user_settings.switch_user(self)
                        break
                    elif pwd == 'shutdown':
                        # Shutting down...
                        shutdown = self.shutdown('db_unprotected.txt')
                        if shutdown == 1:
                            print("\n" * 10)
                            Loading.log("System asleep.")
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        else:
                            return shutdown
                    elif pwd == 'debugexit':
                        # Carryover from original code :)
                        Loading.log("Returned code debug.")
                        return
                    else:
                        print("Sorry, that's the wrong password. Try again.")
                        incorrect_pwd += 1
                        pass
            else:
                while True:
                    # The guest account, housed in its own while loop. The only way to exit is to use debugexit, or when the user shuts down.
                    print("The Guest account will boot into the main screen, but any user settings will have no effect. This includes usernames, passwords, game progress, saved notes, etc. Press [ENTER] or [return] to login")
                    if input() == 'debugexit':
                        return
                    Loading.log("Guest user logged in")
                    self.operating_system()
                    break

    def operating_system(self):
        # The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
        Loading.log(self.current_user.username + " logged in.")
        print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
        while True:
            # Main while loop for applications.
            if self.current_user.elevated:
                print("\nAPPLICATIONS\nUTILITIES\t\t\tGAMES\t\t\tADMIN")
                for i in range(len(self.games)):
                    print(self.utilities[i] + '\t\t' + self.games[i] + '\t\t' + self.admin[i])
            else:
                print("\nAPPLICATIONS\nUTILITIES\t\t\tGAMES")
                for i in range(len(self.games)):
                    print(self.utilities[i] + '\t\t' + self.games[i])
            choice = input().lower()
            # This logs what app the user opened, but the number codes still work.
            Loading.log(self.current_user.username + " opened " + choice)
            # First check if the user is elevated... for reasons.
            if self.current_user.elevated:
                if choice in ('task manager', '7'):
                    TaskManager.main(self.current_user.saved_state)
                elif choice in ('event viewer', 'events'):
                    EventViewer.main()
                elif choice in ('reset', '10'):
                    Reset.user_reset()
                    return 4
            # The if elif else of choices... so long...
            if choice in ('jokes', 'joke', '1', 'joke teller'):
                self.current_user.saved_state['Jokes'] = 'running'
                Jokes.main()
            elif choice in ('notepad', 'notes', 'note', '2'):
                self.current_user.saved_state['Notepad'] = 'running'
                self.notepad.main(self.current_user)
            elif choice in ('speedslow', 'speed up', 'slow down', 'speed up or slow down'):
                self.current_user.saved_state['SpeedSlow'] = 'running'
                SpeedSlow.main()
            elif choice in ('bagels', 'bagels', '3'):
                self.current_user.saved_state["Bagels Game"] = "running"
                self.current_user.bagels.main()
            elif choice in ('tictactoe', 'tic-tac-toe', 'ttt', '4'):
                self.current_user.saved_state["TicTacToe"] = "running"
                self.current_user.ttt = TicTacToe(self.current_user.username)
                self.current_user.ttt.main(self.current_user)
            elif choice in ('hangman', '5'):
                self.current_user.saved_state["Hangman"] = "running"
                self.current_user.hangman.main()
            elif choice in ('sonar', '6'):
                print("Still in progress...")
            elif choice in ('user settings', 'usersettings', '8'):
                self.current_user.saved_state["User Settings"] = "running"
                if self.user_settings.main(self) == 1:
                    return 'regular'
            elif choice in ('system info', 'sys info', '9'):
                self.current_user.saved_state["System Info"] = "running"
                SystemInfo.main(self.versions)
            elif choice in ('exit', 'lock computer', 'lock', '11'):
                Loading.log(self.current_user.username + " logged out.")
                print("Computer has been locked.")
                return 'regular'
            elif choice in ('shutdown', '12', 'power'):
                Loading.log(self.current_user.username + " logged out and shutdown.")
                return self.shutdown('db_unprotected.txt')
            elif choice in ('debugexit', 'debug'):
                return 'regular'

            else:
                print("Please choose from the list of applications.")

    def shutdown(self, unprotected_db_file):
        Loading.log("Preparing to shut down...")
        user_games = open(unprotected_db_file, 'w')
        # The shutdown method. Saves everything to disk and rides return statements all the way back to the main file. Exits safely after that.
        if self.current_user.username == 'Guest':
            input("The guest user cannot save progress. The system will shutdown.")
            return 3
        while True:
            # While loop to choose what type of shutdown to do.
            print("Choose an option.")
            print("1. Sleep\n2. Hibernate\n3. Shutdown\n4. Restart\nType \"info\" for details.")
            shutdown_choice = input().lower()
            if shutdown_choice == "info":
                # Show info
                print("1. Sleep\nSleep does not close the python shell. It logs out the current user and saves the session to RAM. Forcibly closing "
                      "the shell will result in lost data.\n2. Hibernate\nHibernate saves the current session to disk and exits the python shell. "
                      "The python shell is closed and all data is saved.\n3. Shutdown\nShutdown saves only users and notes to disk. All other data "
                      "is erased and all apps are quit.\n4. Restart\nRestart shuts down the computer, saving only users and notes to disk, and opens "
                      "the program again.")
                input()
                pass
            elif shutdown_choice in ("sleep", "1"):
                # Return sleep code.
                Loading.log("The system is now asleep.")
                print("Sleeping...")
                return 1
            elif shutdown_choice in ("hibernate", "2", 'shutdown', '3', 'restart', '4'):
                # Logic for hibernate vs shutdown vs restart.
                hibernate = False
                shutdown = False
                if shutdown_choice in ('hibernate', '2'):
                    print("Hibernating...")
                    hibernate = True
                elif shutdown_choice in ('shutdown', '3', 'restart', '4'):
                    # Logic for shutdown vs restart. Very simple.
                    if shutdown_choice in ('shutdown', '3'):
                        shutdown_choice = 'shutdown'
                        shutdown = True
                        print("Shutting down...")
                    else:
                        shutdown_choice = 'restart'
                        print("Restarting...")
                    # Check if any programs are running
                    program_running = False
                    for i in self.users:
                        for j in i.saved_state:
                            if i.saved_state[j] == 'running':
                                program_running = True
                    for i in self.current_user.saved_state:
                        if i == 'running':
                            print("The " + i + " program is running.")
                            program_running = True
                    if program_running:
                        print("Would you like to force quit these apps?")
                        if input("Type \"{}\" to force quit all apps and proceed with {} or type [ENTER] or [return] to return to the OS.\n".format(shutdown_choice, shutdown_choice)) == 'shutdown':
                            pass
                        else:
                            # Return to allow the user to save their progress.
                            Loading.returning("Returning to the login screen in 3 seconds.", 3)
                            return 0
                    else:
                        print("No apps are open.")
                    Loading.log("All apps closed.")
                    if shutdown_choice in ('shutdown', '3'):
                        print("Shutting down...")
                    else:
                        print("Restarting...")
                    # Proceeding with force quitting and shutting down.
                    self.current_user.saved_state["Jokes"] = self.current_user.saved_state["Notepad"] = self.current_user.saved_state["Bagels Game"] = \
                        self.current_user.saved_state["TicTacToe"] = self.current_user.saved_state["User Settings"] = \
                        self.current_user.saved_state["System Info"] = "not running"
                if hibernate:
                    # Translate all games to be written to disk.
                    Loading.log("Saving game data...")
                    for i in self.users:
                        # Try accessing ttt progress... if not, say nothing.
                        # Special protocol to translate ttt progress lists and strings to strings with splitters for db formatting.
                        translated_board = ''
                        for j in range(8):
                            if i.ttt.board[j] == 'X' or i.ttt.board[j] == 'O':
                                translated_board += (i.ttt.board[j] + ',')
                            else:
                                translated_board += ' ,'
                        i.ttt = translated_board + i.ttt.board[8] + '.' + str(i.ttt.turn) + '.' + i.ttt.player_letter

                        # Now for bagels! Simple Array, no translation needed.
                        i.bagels = i.bagels.last_guess + '.' + i.bagels.num_guesses + '.' + i.bagels.num_digits + '.' + i.bagels.secret_num + '.' + i.bagels.max_guesses

                        # Now for hangman!
                        i.hangman = i.hangman.missed_letters + '.' + i.hangman.correct_letters + '.' + i.hangman.secret_word + '.' + i.hangman.secret_key

                        # Running Programs!
                        translated_save_state = ''
                        for j in i.saved_state:
                            translated_save_state += i.saved_state[j] + '.'
                        i.saved_state = translated_save_state[0:len(translated_save_state) - 1]
                    Loading.log("Game progress saved.")
                # Now write each user's info to their respective info files.
                for i in self.users:
                    # Open their file, write encrypted data and close the file.
                    Loading.log("Updating files...")
                    user_file = open('Users\\' + i.username + '\\info.usrinfo.usr', 'w')
                    user_file.write(Loading.caesar_encrypt(str(i).split('\n', 1)[1] + i.username + '\t\t' + i.password + "\t\t" + str(i.current) + '\t\t') + '\n')
                    user_file.close()
                    if hibernate:
                        user_games.write(i.username + '\t\t' + i.ttt + '\t\t' + i.bagels + '\t\t' + i.hangman + '\t\t' + i.saved_state + '\t\t\n')
                    else:
                        pass
                # Finishing with some print statements.
                Loading.log("Shutdown complete.")
                if hibernate:
                    input('Hibernation complete. Open "{}.py" to restart the system.'.format(self.name))
                    return 2
                elif shutdown:
                    input('Shutdown complete. Open "{}.py" to restart the system.'.format(self.name))
                    return 3
                else:
                    return 4

    def setup(self):
        # The setup method. Conveniently sets up the system to run on its first bootup, and whenever there is no data. Modifies the dictionary with a new user.
        Loading.log("The system has entered SETUP.")
        print("SETUP: Since this is the first time you're running this OS, you have entered the setup.")
        # Ask the user if they want to make a user or not.
        print("Would you like to create a new user, or login as guest?")
        user_or_guest = input()
        if user_or_guest.lower() in ('new user', 'new', 'user', 'yes'):
            # New user it is!
            setup_user = input("Name your user:\n")
            print("New User added. Enter a password or press [ENTER] or [return] to use the default password.")
            while True:
                # The while loop handles the password creation. Can only escape under certain circumstances.
                setup_pwd = input()
                if setup_pwd:
                    # If the user entered a password:
                    print("Password set. Enter it again to confirm it.")
                    if setup_pwd == input():
                        break
                    else:
                        # Handle password matching. Loops back to ensure the user typed the correct passwords.
                        print("The passwords you entered didn't match. Type the same password twice.")
                else:
                    # If the user did not enter a password.
                    self.current_user = User.Administrator(setup_user, 'python123', True)
                    self.users.append(self.current_user)
                    os.mkdir('Users\\' + self.current_user.username)
                    file = open('Users\\' + self.current_user.username + '\\info.usr', 'x')
                    file.close()
                    Loading.returning('Default password set. The password is "python123". Entering startup in 3 seconds.', 3)
                    return
            # User entered password correctly twice.
            self.current_user = User.Administrator(setup_user, setup_pwd, True)
            self.users.append(self.current_user)
            os.mkdir('Users\\{}'.format(self.current_user.username))
            file = open('Users\\{}\\info.usrinfo.usr'.format(self.current_user.username), 'x')
            file.close()
            Loading.returning("Password set successfully. Entering startup in 3 seconds.", 3)
            Loading.log("SETUP is complete. New user has been added. Entering startup.")
            return
        else:
            # If the user did not specify whether they wanted a new user.
            self.current_user = User.Administrator("Guest", "", True)
            self.users.append(self.current_user)
            Loading.returning("Guest user added. There is no password. Press [ENTER] or [return] during login. Entering startup in 3 seconds.", 3)
            Loading.log("SETUP is complete. Guest user has been added. Entering startup.")
            return
