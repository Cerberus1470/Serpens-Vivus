import time

import os
from System import Loading
from System import User
from System import system_recovery
from System.task_manager import TaskManager
from System.reset import Reset
from System.event_viewer import EventViewer
from Applications.jokes import Jokes
from Applications.notepad import Notepad
from Applications.speed_up_or_slow_down import SpeedSlow
from Applications.bagels import Bagels
from Applications.tictactoe import TicTacToe
from Applications.hangman import Hangman
from Applications.sonar import Sonar
from Applications.system_info import SystemInfo
from Applications import user_settings
from Applications.user_settings import UserSettings
import traceback

dirty = []


# noinspection PyBroadException
def boot():
    global dirty
    running = True
    start = time.time()
    dirty = []
    while running:
        try:
            # Initialization reads all files and data from disk and loads it into memory.
            Loading.log("System Startup.")
            if dirty:
                Loading.log("The system is entering Recovery. A fatal internal error has occurred.")
                system_recovery.boot(0, dirty)
                dirty = []
            cerberus = OperatingSystem()
            # Logic to run setup
            if len(cerberus.users) <= 0:
                cerberus.setup()
            # Logic for restarting.
            if cerberus.startup() == 4:
                Loading.returning("Restarting system...", 2)
                Loading.returning("Booting...", 2)
            else:
                running = False
        # Screen for fatal errors. Catches all exceptions and prints the stacktrace. Allows for a reboot.
        except Exception as e:
            for i in range(20):
                print("\n")
            Loading.log("The system encountered a fatal error. Reboot is required. Stacktrace: {}".format(e))

            if input('!!! The system encountered a fatal error. Reboot is required. !!! \nWhat failed: {}\n\nStacktrace: \n{}'.format(
                    str(traceback.format_exc()).split('\n')[len(traceback.format_exc().split('\n'))-4].split('"')[1], str(traceback.format_exc()) + '\nType "REBOOT" to reboot.')) == "REBOOT":
                pass
            else:
                print("Goodbye")
                running = False
        Loading.log("System Shutdown. {} seconds have elapsed.".format(str(time.time() - start)))


# noinspection PyTypeChecker
class OperatingSystem:

    def __init__(self):
        # User list, name, and versions. All inherent settings.
        self.users = []
        self.name = "Cerberus"
        self.dirty = False
        self.recently_deleted_users = []
        self.utilities = ["User Settings", "System Info\t", "Notepad\t\t", "SpeedSlow\t", "\t\t\t"]
        self.games = ["Bagels\t", "TicTacToe", "Hangman ", "Sonar", "Joke Teller"]
        self.admin = ["Reset\t\t", "Event Viewer\t", "Task Manager", "\t\t", "\t\t"]
        self.versions = {"Main": 5.4, "Joke Teller": 1.4, "Notepad": 3.3, "Bagels": 4.5, "TicTacToe": 5.7, "Hangman": 3.5, "Sonar": 2.1, "User Settings": 2.9, "System Info": 1.6, "Event Viewer": 1.1, "SpeedSlow": 1.2, "System Recovery": 1.0}
        self.path = "Users\\{}"
        self.reload()
        # The main boot sequence. Reading from user folder and readying lines of decrypted user info.
        # lines = []
        # Loading.log("Reading info from memory...")
        # # Looping through the User folders to read their info files.
        # for subdir, dirs, files in os.walk('Users'):
        #     for dir1 in dirs:
        #         try:
        #             # The first of many user files...
        #             file = open(self.path.format(dir1) + "\\info.usr", 'r')
        #             file1 = list(file)
        #             lines.append([Loading.caesar_decrypt(file1[0].split('\n')[0]), Loading.caesar_decrypt(file1[1].split('\n')[0])])
        #             file.close()
        #         except FileNotFoundError:
        #             continue
        # Loading.log("Decryption complete.")
        # for i in lines:
        #     # Ready the sections!
        #     sections = ['USER TYPE', 'USERNAME', 'PASSWORD', 'CURRENT STATUS']
        #     progress = 0
        #     user_info = ['', '', '', '']
        #     try:
        #         # First save the user type. (Standard vs Admin)
        #         (user_info[0], rest) = i[0].split('\t\t', 1)
        #         # Now loop for 4 more blocks, tracking progress so the user is alerted about corruption.
        #         for j in range(1, 4):
        #             progress = j
        #             (user_info[j], rest) = rest.split('\t\t', 1)
        #             pass
        #     except ValueError:
        #         # If something is missing, log the event.
        #         Loading.log("A user file is corrupted at the {} section.".format(sections[progress]))
        #         user_info[progress] = 'INVALID'
        #     if user_info[0] == 'StandardUser':
        #         self.users.append(User.StandardUser(user_info[1], user_info[2], user_info[3] == "True"))
        #     else:
        #         self.users.append(User.Administrator(user_info[1], user_info[2], user_info[3] == "True"))
        #     if i[1]:
        #         self.users[lines.index(i)].saved_state = {}
        #         apps = (bagels, hangman, jokes, notepad, sonar, speedslow, system_info, tictactoe, user_settings)
        #         for j in apps:
        #             self.users[lines.index(i)].saved_state[j] = i[1].split('.')[apps.index(j)]
        #             # {bagels: i[1].split('.')[0], hangman: i[1].split('.')[1], jokes: i[1].split('.')[2],
        #             #  notepad: i[1].split('.')[3], sonar: i[1].split('.')[4], speedslow: i[1].split('.')[5],
        #             #  system_info: i[1].split('.')[6], tictactoe: i[1].split('.')[7], user_settings: i[1].split('.')[8]}
        #         if self.users[lines.index(i)].elevated:
        #             self.users[lines.index(i)].saved_state[task_manager] = i[1].split('.')[9]
        #             self.users[lines.index(i)].saved_state[event_viewer] = i[1].split('.')[10]
        #     else:
        #         self.users[lines.index(i)].saved_state["Bagels"] = self.users[lines.index(i)].saved_state["Hangman"] = \
        #             self.users[lines.index(i)].saved_state["Jokes"] = self.users[lines.index(i)].saved_state["Notepad"] = \
        #             self.users[lines.index(i)].saved_state["Sonar"] = self.users[lines.index(i)].saved_state["SpeedSlow"] = \
        #             self.users[lines.index(i)].saved_state["System Info"] = self.users[lines.index(i)].saved_state["TicTacToe"] = \
        #             self.users[lines.index(i)].saved_state["User Settings"] = "not running"
        #         if self.users[lines.index(i)].elevated:
        #             self.users[lines.index(i)].saved_state["Task Manager"] = \
        #                 self.users[lines.index(i)].saved_state["Event Viewer"] = "not running"
        # Loading.log("The protected database is finished.")
        # Setting the current user object.
        for j in range(len(self.users)):
            if self.users[j].current:
                self.current_user = self.users[j]
                break
        Loading.log("Boot complete.")
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.name + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
               self.current_user.username + "\n Current Password is hidden. >"

    def reload(self):
        global dirty
        try:
            new_users = []
            for subdir, dirs, files in os.walk("Users"):
                if "info.usr" in files:
                    file = list(open("{}\\info.usr".format(subdir), 'r'))
                    info = Loading.caesar_decrypt(file[0]).split('\t\t')
                    programs = Loading.caesar_decrypt(file[1]).split('.')
                    if len(info) == 5 and (len(programs) == 1 or len(programs) == 9 or len(programs) == 11):
                        if info[0] == "StandardUser":
                            new_users.append(User.StandardUser(info[1], info[2], info[3] == "True", programs))
                        elif info[0] == "Administrator":
                            new_users.append(User.Administrator(info[1], info[2], info[3] == "True", programs))
                        else:
                            dirty.append(subdir)
                            raise IndexError
                    else:
                        dirty.append(subdir)
                        raise IndexError
            self.users = new_users
        except IndexError:
            raise Loading.CorruptedFileSystem("The file system is corrupted. Please reboot safely.")

    def startup(self):
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
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
                        UserSettings.switch_user(self)
                        break
                    elif pwd in ('shutdown', 'power'):
                        # Shutting down...
                        shutdown = self.shutdown()
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
            print("\nLock Computer\tPower")
            choice = input().lower()
            # This logs what app the user opened, but the number codes still work.
            Loading.log(self.current_user.username + " opened " + choice)
            choices_list = {Jokes: ('jokes', 'joke', '1', 'joke teller'), Notepad: ('notepad', 'notes', 'note', '2')
                            , SpeedSlow: ('speedslow', 'speed up', 'slow down', 'speed up or slow down')
                            , Bagels: ('bagels', 'bagels', '3'), TicTacToe: ('tictactoe', 'tic-tac-toe', 'ttt', '4')
                            , Hangman: ('hangman', '5'), Sonar: ('sonar', '6'), user_settings: ('user settings', 'usersettings', '8')
                            , SystemInfo: ('system info', 'sys info', '9'), TaskManager: ('task manager', '7')
                            , EventViewer: ('event viewer', 'events'), Reset: ('reset', '10')}
            if choice in ('exit', 'lock computer', 'lock', '11'):
                Loading.log(self.current_user.username + " logged out.")
                print("Computer has been locked.")
                return 'regular'
            elif choice in ('shutdown', '12', 'power'):
                Loading.log(self.current_user.username + " logged out and shutdown.")
                return self.shutdown()
            elif choice in ('debugexit', 'debug'):
                return 'regular'
            choice_in_list = False
            for i in choices_list:
                if choice in choices_list[i]:
                    choice_in_list = True
                    self.current_user.saved_state[i] = "running"
                    if list(choices_list.keys()).index(i) >= len(choices_list) - 3:
                        if self.current_user.elevated:
                            if i.boot(self) == 4:
                                return 4
                    else:
                        if i.category == "games":
                            if i.boot(self.path.format(self.current_user.username)) == 'regular':
                                print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                                return 'regular'
                        elif i.category == "utilities":
                            if i.boot(self) == 'regular':
                                print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                                return 'regular'
                    break
            if not choice_in_list:
                Loading.returning("Please choose from the list of applications.", 1)

    def shutdown(self):
        Loading.log("Preparing to shut down...")
        # The shutdown method. Saves everything to disk and rides return statements all the way back to the main file. Exits safely after that.
        if self.current_user.username == 'Guest':
            Loading.returning("The guest user cannot save progress. The system will shutdown.", 3)
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
                    program_count = 0
                    for i in self.users:
                        for j in i.saved_state:
                            if i.current:
                                if self.current_user.saved_state[j] == 'running':
                                    program_count += 1
                            elif i.saved_state[j] == "running":
                                i.saved_state[j] = "not running"
                    if program_count > 0:
                        print("Waiting for {} programs to close.".format(program_count))
                        for i in self.current_user.saved_state:
                            if self.current_user.saved_state[i] == 'running':
                                self.current_user.saved_state[i] = "not running"
                                Loading.returning("Closing {}.".format(str(i.__name__)), 2)
                        if shutdown_choice in ('shutdown', '3'):
                            print("Shutting down...")
                        else:
                            print("Restarting...")
                        Loading.log("All apps closed.")
                    else:
                        print("No apps are open.")
                for i in self.users:
                    # Running Programs!
                    i.saved_state = '.'.join(i.saved_state.values())
                # Now write each user's info to their respective info files.
                for i in self.users:
                    # Open their file, write encrypted data and close the file.
                    Loading.log("Updating user files...")
                    user_file = open(self.path.format(i.username) + "\\info.usr", 'w')
                    user_file.write(Loading.caesar_encrypt(i.__class__.__name__ + '\t\t' + i.username + '\t\t' + i.password + "\t\t" + str(i.current) + '\t\t\n'))
                    user_file.write(Loading.caesar_encrypt(i.saved_state + '\n'))
                    user_file.close()
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
            else:
                print("Please choose from the list of choices.")

    def setup(self):
        # The setup method. Conveniently sets up the system to run on its first boot, and whenever there is no data. Modifies the dictionary with a new user.
        Loading.log("The system has entered SETUP.")
        try:
            os.mkdir("Users")
        except FileExistsError:
            raise Loading.CorruptedFileSystem("The file structure is corrupted.")
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
                    os.mkdir(self.path.format(self.current_user.username))
                    file = open(self.path.format(self.current_user.username) + '\\info.usr', 'x')
                    file.close()
                    Loading.returning('Default password set. The password is "python123". Entering startup in 3 seconds.', 3)
                    return
            # User entered password correctly twice.
            self.current_user = User.Administrator(setup_user, setup_pwd, True)
            self.users.append(self.current_user)
            os.mkdir('Users\\{}'.format(self.current_user.username))
            file = open(self.path.format(self.current_user.username) + "\\info.usr", 'w')
            file.write(Loading.caesar_encrypt(self.current_user.__class__.__name__ + '\t\t' + self.current_user.username + '\t\t' + self.current_user.password + "\t\t" + str(self.current_user.current) + '\t\t\n\n'))
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
