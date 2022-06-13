import time

import os
import random
from System import Loading
from System.User import *
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
from Applications.user_settings import UserSettings
import traceback
from tkinter import *
from tkinter.ttk import *

dirty = []


# noinspection PyBroadException
def boot():
    global dirty
    running = True
    start = time.time()
    dirty = []
    cerberus = OperatingSystem()
    while running:
        try:
            # Initialization reads all files and data from disk and loads it into memory.
            Loading.log("System Startup.")
            if cerberus.error:
                Loading.returning("Entering Recovery...", 1)
                system_recovery.SystemRecovery.boot(cerberus.error)
                Loading.returning("Saving changes and booting...", 3)
                print('\n\n\n\n\n')
            cerberus.reload()
            # Logic to run setup

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
            Loading.log("{} encountered a fatal error. Reboot is required. Stacktrace: {}".format(cerberus.name, e))
            if input('!!! {} encountered a fatal error. Reboot is required. !!! \nWhat failed: {}\n\nStacktrace: \n{}'.format(
                    cerberus.name, str(traceback.format_exc()).split('\n')[len(traceback.format_exc().split('\n')) - 4].split('"')[1], str(traceback.format_exc())) + '\nType "REBOOT" to reboot.') == "REBOOT":
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
        self.error = []
        self.recently_deleted_users = []
        self.versions = {"Main": 6.0, "Joke Teller": 1.4, "Notepad": 3.3, "Bagels": 4.5, "TicTacToe": 5.7, "Hangman": 3.5, "Sonar": 2.1, "User Settings": 2.9, "System Info": 1.6, "Event Viewer": 1.1, "SpeedSlow": 1.2, "System Recovery": 1.0}
        self.path = "Users\\{}"
        self.current_user = User()
        Loading.log("Boot complete.")

        self.tk = Tk()
        self.pwd_var = StringVar()
        self.incorrect_pwd = 0
        self.startup_window = Toplevel(self.tk)
        self.desktop_window = Toplevel(self.tk)
        self.shutdown_window = Toplevel(self.tk)
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.name + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
               self.current_user.username + "\n Current Password is hidden. >"

    # noinspection PyUnreachableCode
    def reload(self):
        global dirty
        self.error = []
        new_users = []
        for subdir, dirs, files in os.walk("Users"):
            if len(dirs) == 0 and len(files) == 0:
                self.setup()
                return
            if "info.usr" in files:
                file = list(open("{}\\info.usr".format(subdir), 'r'))
                info = Loading.caesar_decrypt(file[0]).split('\t\t')
                programs = Loading.caesar_decrypt(file[1]).split('\t\t')
                if len(info) == 5 and (len(programs) == 1 or len(programs) == 10 or len(programs) == 12):
                    try:
                        new_users.append(globals()[info[0]](info[1], info[2], info[3] == "True", programs))
                    except (AttributeError, IndexError):
                        self.error.append(system_recovery.CorruptedFileSystem([subdir, info, programs]))
                else:
                    self.error.append(system_recovery.CorruptedFileSystem([subdir, info, programs]))
        if new_users or self.error:
            # Setting the current user object.
            admin_present = False
            self.users = new_users
            for j in self.users:
                if j.current:
                    self.current_user = j
                if j.elevated:
                    admin_present = True
            if new_users:
                if self.current_user.username == "Default" and self.current_user.password == "Default" and self.current_user.__class__.__name__ == "User":
                    self.error.append(system_recovery.NoCurrentUser())
                if not admin_present:
                    self.error.append(system_recovery.NoAdministrator())
            if self.error:
                if len(self.error) == 1:
                    raise Exception(self.error[0].__repr__() + " Please reboot the system.")
                else:
                    raise Exception("Multiple fatal errors occurred. Please reboot the system.")
        else:
            self.setup()
            return

    def startup(self):
        for i in (self.tk, self.desktop_window, self.shutdown_window):
            if i:
                i.withdraw()
        self.pwd_var.set('')
        self.startup_window.geometry('520x180')
        Label(self.startup_window, text='Hello! I am Cerberus. Current user: ' + self.current_user.username + '.').place(x=50, y=30)
        Label(self.startup_window, text="Password:").place(x=50, y=60)
        Entry(self.startup_window, width="55", textvariable=self.pwd_var).place(x=110, y=60)
        Button(self.startup_window, text="Log in", command=lambda: self.login(self.pwd_var.get())).place(x=50, y=90)
        Button(self.startup_window, text="Switch Users", command=lambda: self.login("switch")).place(x=150, y=90)
        Button(self.startup_window, text="Power", command=lambda: self.login("power")).place(x=250, y=90)
        self.startup_window.deiconify()
        self.startup_window.mainloop()

    def login(self, password=''):
        print(password)
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        if self.current_user.username != 'Guest':
            if self.incorrect_pwd >= 2:
                strike_three = Label(self.startup_window, text="You have incorrectly entered the password 3 times. The computer will now restart.")
                strike_three.place(x=50, y=120)
                strike_three.after(5000, self.startup_window.destroy)
            if password == self.current_user.password:
                self.startup_window.withdraw()
                # Move to the system screen.
                self.desktop()
                # Loading.log("Code {} returned. Executing task.".format(os_rv))
                # # Logic for returning from the OS screen.
                # if os_rv == 1:
                #     print("\n" * 10)
                #     print("The System is sleeping. Press [ENTER] or [return] to wake.")
                #     input()
                # elif os_rv == 'regular':
                #     pass
                # else:
                #     return os_rv
            elif password == 'debugexit':
                # Carryover from original code :)
                Loading.log("Returned code debug.")
                return
            else:
                self.incorrect_pwd += 1
                welcome = Label(self.startup_window, text="Sorry, that's the wrong password. Try again.\t\tIncorrect Attempts: " + str(self.incorrect_pwd))
                welcome.place(x=50, y=120)
                welcome.after(3000, welcome.destroy)
                print("Sorry, that's the wrong password. Try again.")
                pass
        else:
            while True:
                # The guest account, housed in its own while loop. The only way to exit is to use debugexit, or when the user shuts down.
                print("WARNING: The Guest account will boot into the main screen, but any user settings or games will have no effect. \nThis includes usernames, passwords, game progress, saved notes, etc.")
                print("All games will say that the file or path is not found, this is normal. The Guest User doesn't have a user folder.\nPress [ENTER] or [return] to login.")
                if input() == 'debugexit':
                    return
                Loading.log("Guest user logged in")
                self.desktop()
                return 3

    def desktop(self):
        # The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
        Loading.log(self.current_user.username + " logged in.")
        self.desktop_window.title("Cerberus - Desktop")
        self.desktop_window.geometry('425x225')
        hello = Label(self.desktop_window, text="\t\tHello! I am {}, running POCS v{}\n\nAPPLICATIONS".format(self.name, self.versions["Main"]))
        hello.place(x=10, y=10)
        print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
        # Main while loop for applications.
        apps_frame = Frame(self.desktop_window)
        apps_frame.place(x=10, y=60)
        utilities_title = Label(apps_frame, text='UTILITIES')
        utilities_title.grid(row=0, column=0, padx=10)
        games_title = Label(apps_frame, text='GAMES')
        games_title.grid(row=0, column=1, padx=10)
        apps = [[UserSettings, SystemInfo, Notepad, SpeedSlow], [Bagels, TicTacToe, Hangman, Sonar, Jokes], [Reset, EventViewer, TaskManager]]
        for i in range(len(apps)):
            if i == 2:
                if self.current_user.elevated:
                    for j in range(len(apps[i])):
                        Button(apps_frame, text=apps[i][j].name, command=lambda a=i, b=j: self.select_app(apps[a][b])).grid(row=j + 1, column=i, padx=10)
            else:
                for j in range(len(apps[i])):
                    Button(apps_frame, text=apps[i][j].name, command=lambda a=i, b=j: self.select_app(apps[a][b])).grid(row=j + 1, column=i, padx=10)
        Button(apps_frame, text='Lock Computer', command=lambda: self.lock()).grid(row=0, column=4)
        Button(apps_frame, text='Power', command=lambda: self.power()).grid(row=1, column=4)
        if self.current_user.elevated:
            admin_title = Label(apps_frame, text='ADMIN')
            admin_title.grid(row=0, column=2, padx=10)
        #     print("\nAPPLICATIONS\nUTILITIES\t\t\tGAMES\t\t\tADMIN")
        #     for i in range(len(self.games)):
        #         print(self.utilities[i] + '\t\t' + self.games[i] + '\t\t' + self.admin[i])
        # else:
        #     print("\nAPPLICATIONS\nUTILITIES\t\t\tGAMES")
        #     for i in range(len(self.games)):
        #         print(self.utilities[i] + '\t\t' + self.games[i])
        print("\nLock Computer\tPower")
        self.desktop_window.deiconify()
        choice = ''
        # input().lower()
        # This logs what app the user opened, but the number codes still work.
        Loading.log(self.current_user.username + " opened " + choice)

    def lock(self):
        self.desktop_window.withdraw()
        self.startup()

    def power(self):
        self.desktop_window.withdraw()
        self.shutdown()

    def select_app(self, choice):
        match choice:
            case 'debug':
                return 'regular'
        choices_list = [Jokes, Notepad, SpeedSlow, Bagels, TicTacToe, Hangman, Sonar, UserSettings, SystemInfo, TaskManager, EventViewer, Reset]
        for i in choices_list:
            if choice == i:
                self.current_user.saved_state[i] = True
                if i.category == "games":
                    if i.boot(self.path.format(self.current_user.username)) == 'regular':
                        print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                        return 'regular'
                elif i.category == "utilities":
                    if i.boot(self) == 'regular':
                        print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                        return 'regular'
                break
        else:

            Loading.returning("Please choose from the list of applications.")

    def shutdown(self):
        Loading.log("Preparing to shut down...")
        # The shutdown method. Saves everything to disk and rides return statements all the way back to the main file. Exits safely after that.
        if self.current_user.username == 'Guest':
            Loading.returning("The guest user cannot save progress. The system will shutdown.", 3)
            return 3
        # While loop to choose what type of shutdown to do.
        self.shutdown_window.geometry("50x185")
        for i in ["Sleep", "Hibernate", "Shutdown", "Restart"]:
            Button(self.shutdown_window, text=i, command=lambda a=i: self.select_shutdown(a.lower())).place(x=20, y=10 + (30 * ["Sleep", "Hibernate", "Shutdown", "Restart"].index(i)))
        Button(self.shutdown_window, text="Info", command=lambda: self.select_shutdown("info")).place(x=20, y=150)
        self.shutdown_window.deiconify()
        print("Choose an option.")
        print("1. Sleep\n2. Hibernate\n3. Shutdown\n4. Restart\nType \"info\" for details.")
        shutdown_choice = None
        # input().lower()

    def select_shutdown(self, shutdown_choice):
        match shutdown_choice:
            case "info":
                # Show info
                infoPanel = Toplevel(self.tk)
                infoPanel.geometry('770x150')
                Label(infoPanel, text="1. Sleep\nSleep does not close the python shell. It logs out the current user and saves the session to RAM. Forcibly closing "
                                      "the shell will result in lost data.\n2. Hibernate\nHibernate saves the current session to disk and exits the python shell. "
                                      "The python shell is closed and all data is saved.\n3. Shutdown\nShutdown saves only users and notes to disk. All other data "
                                      "is erased and all apps are quit.\n4. Restart\nRestart shuts down the computer, saving only users and notes to disk, and opens "
                                      "the program again.").place(x=10, y=10)
                print("1. Sleep\nSleep does not close the python shell. It logs out the current user and saves the session to RAM. Forcibly closing "
                      "the shell will result in lost data.\n2. Hibernate\nHibernate saves the current session to disk and exits the python shell. "
                      "The python shell is closed and all data is saved.\n3. Shutdown\nShutdown saves only users and notes to disk. All other data "
                      "is erased and all apps are quit.\n4. Restart\nRestart shuts down the computer, saving only users and notes to disk, and opens "
                      "the program again.")
                pass
            case "sleep":
                # Return sleep code.
                Loading.log("The system is now asleep.")
                print("Sleeping...")
                self.shutdown_window.withdraw()
                self.startup_window.withdraw()
                sleep_window = Toplevel(self.tk)
                sleep_window.geometry("300x150")
                Label(sleep_window, text="The system is asleep.").place(x=10, y=10)
                Button(sleep_window, text="Wake", command=lambda: self.wake(sleep_window)).place(x=10, y=30)
                return 1
            case ("hibernate", "shutdown", "restart"):
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
                                if self.current_user.saved_state[j]:
                                    program_count += 1
                            elif i.saved_state[j]:
                                i.saved_state[j] = False
                    if program_count > 0:
                        print("Waiting for {} programs to close.".format(program_count))
                        for i in self.current_user.saved_state:
                            if self.current_user.saved_state[i]:
                                self.current_user.saved_state[i] = False
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
                    i.saved_state = '\t\t'.join([str(j) for j in i.saved_state.values()]) + '\t\t\n'
                # Now write each user's info to their respective info files.
                for i in self.users:
                    # Open their file, write encrypted data and close the file.
                    Loading.log("Updating user files...")
                    user_file = open(self.path.format(i.username) + "\\info.usr", 'w')
                    user_file.write(Loading.caesar_encrypt(i.__class__.__name__ + '\t\t' + i.username + '\t\t' + i.password + "\t\t" + str(i.current) + '\t\t\n'))
                    user_file.write(Loading.caesar_encrypt(i.saved_state))
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
            case _:
                print("Please choose from the list of choices.")

    def wake(self, window):
        window.withdraw()
        self.startup()

    def setup(self):
        # The setup method. Conveniently sets up the system to run on its first boot, and whenever there is no data. Modifies the dictionary with a new user.
        Loading.log("The system has entered SETUP.")
        try:
            os.mkdir("Users")
        except FileExistsError:
            pass
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
                    setup_pwd = "python123"
                    Loading.returning('Default password set. The password is "python123".', 2)
                    break
            # User entered password correctly twice.
            self.current_user = Administrator(setup_user, setup_pwd, True)
            Loading.returning("Password set successfully.", 2)
            Loading.returning("One last thing!", 1)
            recovery_pwd = ''.join(str(random.choice(Loading.alphabet)) for _ in range(1000)) + '\t\t' + input("Please enter a recovery password.") + '\t\t' + ''.join(str(random.choice(Loading.alphabet)) for _ in range(1000))
            file = open("System\\recovery.info", 'w')
            file.write(Loading.caesar_encrypt(recovery_pwd))
            file.close()
            self.users.append(self.current_user)
            os.mkdir(self.path.format(self.current_user.username))
            file = open(self.path.format(self.current_user.username) + "\\info.usr", 'w')
            file.write(Loading.caesar_encrypt(self.current_user.__class__.__name__ + '\t\t' + self.current_user.username + '\t\t' + self.current_user.password + "\t\t" + str(self.current_user.current) + '\t\t\n\n'))
            file.close()
            Loading.returning("Entering startup in 3 seconds.", 3)
        else:
            # If the user did not specify whether they wanted a new user.
            self.current_user = Administrator("Guest", "", True)
            self.users.append(self.current_user)
            Loading.returning("Guest user added. There is no password. Entering startup in 3 seconds.", 3)
            os.rmdir("Users")
        Loading.log("SETUP is complete. Entering startup.")
        return
