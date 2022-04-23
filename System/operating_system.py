import time

import os
from System import Loading
from System import User
import System.task_manager as task_manager
import System.reset as reset
import System.event_viewer as event_viewer
import Applications.jokes as jokes
import Applications.notepad as notepad
import Applications.speed_up_or_slow_down as speedslow
import Applications.bagels as bagels
import Applications.tictactoe as tictactoe
import Applications.hangman as hangman
import Applications.sonar as sonar
import Applications.user_settings as user_settings
from Applications.user_settings import UserSettings
import Applications.system_info as system_info
import traceback


# noinspection PyBroadException
def boot():
    running = True
    start = time.time()
    while running:
        try:
            # Initialization reads all files and data from disk and loads it into memory.
            Loading.log("System Startup.")
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
        except Exception as e:
            for i in range(20):
                print("\n")
            Loading.log("The system encountered a fatal error. Reboot is required. Stacktrace: {}".format(e))
            if input('!!! The system encountered a fatal error. Reboot is required. !!! \nWhat failed: {}\n\nStacktrace: {}'.format(e, str(traceback.format_exc()) + '\nType "REBOOT" to reboot.')) == "REBOOT":
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
        self.notepad = ""
        self.utilities = ["User Settings", "System Info\t", "Notepad\t\t", "SpeedSlow\t"]
        self.games = ["Bagels\t", "TicTacToe", "Hangman ", "Joke Teller"]
        self.admin = ["Reset\t\t", "Event Viewer\t", "Task Manager", '\t\t']
        self.versions = {"Main": 5.0, "Joke Teller": 1.3, "Notepad": 3.2, "Bagels": 3.5, "TicTacToe": 4.7, "Hangman": 2.5, "Sonar": 1.0, "User Settings": 2.7, "System Info": 1.5, "Event Viewer": 1.0, "SpeedSlow": 1.1}
        self.user_settings = UserSettings()

        # The main boot sequence.
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
                        file1 = list(file)
                        lines.append([Loading.caesar_decrypt(file1[0].split('\n')[0]), Loading.caesar_decrypt(file1[1].split('\n')[0])])
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
                    (user_info[0], rest) = i[0].split('\t\t', 1)
                    # Now loop for 4 more blocks, tracking progress so the user is alerted about corruption.
                    for j in range(1, 4):
                        progress = j
                        (user_info[j], rest) = rest.split('\t\t', 1)
                        pass
                except ValueError:
                    # If something is missing, log the event.
                    Loading.log("A user file is corrupted at the {} section.".format(sections[progress]))
                    user_info[progress] = 'INVALID'
                if user_info[0] == 'StandardUser':
                    self.users.append(User.StandardUser(user_info[1], user_info[2], user_info[3] == "True"))
                else:
                    self.users.append(User.Administrator(user_info[1], user_info[2], user_info[3] == "True"))
                if i[1]:
                    self.users[lines.index(i)].saved_state = \
                        {"Bagels": i[1].split('.')[0], "Hangman": i[1].split('.')[1], "Jokes": i[1].split('.')[2],
                         "Notepad": i[1].split('.')[3], "Sonar": i[1].split('.')[4], "SpeedSlow": i[1].split('.')[5],
                         "System Info": i[1].split('.')[6], "TicTacToe": i[1].split('.')[7], "User Settings": i[1].split('.')[8]}
                    if self.users[lines.index(i)].elevated:
                        self.users[lines.index(i)].saved_state["Task Manager"] = i[1].split('.')[9]
                        self.users[lines.index(i)].saved_state["Event Viewer"] = i[1].split('.')[10]
                else:
                    self.users[lines.index(i)].saved_state["Bagels"] = self.users[lines.index(i)].saved_state["Hangman"] = \
                        self.users[lines.index(i)].saved_state["Jokes"] = self.users[lines.index(i)].saved_state["Notepad"] = \
                        self.users[lines.index(i)].saved_state["Sonar"] = self.users[lines.index(i)].saved_state["SpeedSlow"] = \
                        self.users[lines.index(i)].saved_state["System Info"] = self.users[lines.index(i)].saved_state["TicTacToe"] = \
                        self.users[lines.index(i)].saved_state["User Settings"] = "not running"
                    if self.users[lines.index(i)].elevated:
                        self.users[lines.index(i)].saved_state["Task Manager"] = \
                            self.users[lines.index(i)].saved_state["Event Viewer"] = "not running"
            Loading.log("The protected database is finished.")
            # Setting the current user object.
            for j in range(len(self.users)):
                if self.users[j].current:
                    self.current_user = self.users[j]
                    break
            pass
        Loading.log("Boot complete.")
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.name + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
               self.current_user.username + "\n Current Password is hidden. >"

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
                        self.user_settings.switch_user(self)
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
            choices_list = {jokes: ('jokes', 'joke', '1', 'joke teller'), notepad: ('notepad', 'notes', 'note', '2')
                            , speedslow: ('speedslow', 'speed up', 'slow down', 'speed up or slow down')
                            , bagels: ('bagels', 'bagels', '3'), tictactoe: ('tictactoe', 'tic-tac-toe', 'ttt', '4')
                            , hangman: ('hangman', '5'), sonar: ('sonar', '6'), user_settings: ('user settings', 'usersettings', '8')
                            , system_info: ('system info', 'sys info', '9'), task_manager: ('task manager', '7')
                            , event_viewer: ('event viewer', 'events'), reset: ('reset', '10')}
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
                    if list(choices_list.keys()).index(i) >= len(choices_list) - 3:
                        if self.current_user.elevated:
                            if i.boot(self) == 4:
                                return 4
                    else:
                        if i.boot(self) == 'regular':
                            print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                            return 'regular'
                    break
            if not choice_in_list:
                Loading.returning("Please choose from the list of applications.", 2)

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
                    for i in self.current_user.saved_state:
                        if self.current_user.saved_state[i] == 'running':
                            program_count += 1
                    if program_count > 0:
                        print("Waiting for {} programs to close.".format(program_count))
                        for i in self.current_user.saved_state:
                            if self.current_user.saved_state[i] == 'running':
                                Loading.returning("Closing {}.".format(str(i)), 2)
                        if shutdown_choice in ('shutdown', '3'):
                            print("Shutting down...")
                        else:
                            print("Restarting...")
                        Loading.log("All apps closed.")
                    else:
                        print("No apps are open.")
                if hibernate:
                    for i in self.users:
                        # Running Programs!
                        translated_save_state = ''
                        for j in i.saved_state:
                            translated_save_state += i.saved_state[j] + '.'
                        i.saved_state = translated_save_state[0:len(translated_save_state) - 1]
                    Loading.log("Game progress saved.")
                # Now write each user's info to their respective info files.
                for i in self.users:
                    # Open their file, write encrypted data and close the file.
                    Loading.log("Updating user files...")
                    user_file = open('Users\\' + i.username + '\\info.usr', 'w')
                    user_file.write(Loading.caesar_encrypt(str(i).split('\n', 1)[1] + i.username + '\t\t' + i.password + "\t\t" + str(i.current) + '\t\t\n'))
                    if hibernate:
                        user_file.write(Loading.caesar_encrypt(i.saved_state + '\n'))
                    else:
                        user_file.write('\n')
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
            file = open('Users\\{}\\info.usr'.format(self.current_user.username), 'x')
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
