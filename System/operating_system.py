"""
Module operating_system. This module contains the Core Python OS functions and classes. Probably the most complex file in the system.
"""
import colorama
import maskpass
import requests
import traceback

try:
    from Applications.bagels import Bagels
    from Applications.event_viewer import EventViewer
    from Applications.hangman import Hangman
    from Applications.jokes import Jokes
    from Applications.notepad import Notepad
    from Applications.scout_rpg import ScoutRpg
    from Applications.sonar import Sonar
    from Applications.speed_up_or_slow_down import SpeedUpOrSlowDown
    from Applications.system_info import SystemInfo
    from Applications.task_manager import TaskManager
    from Applications.tictactoe import Tictactoe
    from Applications.settings import Settings
    from Applications.user_settings import UserSettings
    from System import Loading
    from System import system_recovery
    from System.User import *
    from System.reset import Reset
except ImportError as missing_files:
    Bagels = EventViewer = Hangman = Jokes = Notepad = ScoutRpg = Sonar = SpeedUpOrSlowDown = SystemInfo = TaskManager = \
        Tictactoe = UserSettings = system_recovery = Reset = Settings = None
    # If any file is missing, code will come here.
    # UPDATE Change whenever the token changes!
    token = "DOESN'T WORK"
    for folder in (("System/", ("Loading.py", "operating_system.py", "reset.py", "system_recovery.py", "User.py")),
                   ("Applications/", ("bagels.py", "event_viewer.py", "hangman.py", "jokes.py", "notepad.py", "scout_rpg.py", "settings.py",
                                      "sonar.py", "speed_up_or_slow_down.py", "sudoku.py", "system_info.py", "task_manager.py",
                                      "tictactoe.py", "user_settings.py"))):
        for filename in folder[1]:
            try:
                file = open("{}/{}".format(folder[0], filename), 'x', encoding='utf-8')
                download = requests.get("https://raw.githubusercontent.com/Cerberus1470/Sentiens-Anguis/Tejas/{}/{}".format(folder[0], filename),
                                        headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
                file.write(download.content.decode())
                file.close()
            except FileExistsError:
                pass
    from System import Loading

    Loading.returning("The system is missing files. It will now re-download them from GitHub. Please wait.", 4)
    Loading.progress_bar("Downloading Files", 5)
    Loading.returning("The system has finished downloading/updating files and will now reboot", 5)

# Public Variables
user_separator = "(U)"
program_separator = "(P)"
personalization_separator = "(Pe)"


# noinspection PyBroadException
def boot(error=True, stacktrace=False):
    """
    Method boot(). This method regulates the boot process of the Core OS. It is responsible for allowing one-line startup.
    :return: 0 if no crashes occur. Code 1-4 if an error occurs.
    """
    running = True
    OperatingSystem.HANDLE_ERROR = error
    colorama.just_fix_windows_console()
    start = time.time()
    cerberus = OperatingSystem()
    Loading.log("System Startup.")
    while running:
        try:
            # This code catches any boot errors.
            if cerberus.error:
                system_recovery.SystemRecovery.boot(cerberus.error)
            cerberus.reload()
            # Logic for restarting.
            if cerberus.startup() == 4:
                Loading.returning("Restarting system...", 2)
                Loading.returning("Booting...", 2)
            else:
                return "Code 0. Execution successful."
        # Screen for fatal errors. Catches all exceptions and prints the stacktrace. Allows for a reboot.
        except Exception as fatal_error:
            if not OperatingSystem.HANDLE_ERROR:
                raise fatal_error
            Loading.log(
                "{} encountered a fatal error. Reboot is required. Stacktrace: {}".format(cerberus.name,
                                                                                          fatal_error if stacktrace else "Stacktrace disabled"))
            if stacktrace:
                try:
                    if input(
                            '{}!!! {} encountered a fatal error. Reboot is required. !!! \nWhat failed: {}\n\nStacktrace: \n{}'
                            ''.format('\n' * 20, cerberus.name,
                                      str(traceback.format_exc()).split('\n')[
                                          len(traceback.format_exc().split('\n')) - 4].split(
                                          '"')[1],
                                      str(traceback.format_exc())) + '\nType "REBOOT" to reboot.') == "REBOOT":
                        continue
                    break
                except IndexError:
                    pass
            if input(
                    '!!! {} encountered a fatal error. Reboot is required. !!! Type "REBOOT" to reboot'.format(
                        cerberus.name)):
                continue
            print("Goodbye")
            return "Code {}. A system error has occurred.".format(','.join([str(i.code) for i in cerberus.error]) if cerberus.error else "-1")
        Loading.log("System Shutdown. {} seconds have elapsed.".format(str(time.time() - start)))
    return


# noinspection PyTypeChecker,PyBroadException
class OperatingSystem:
    """
    Class Operating System. Houses all the core functions aside from boot.
    """
    HANDLE_ERROR = True

    def __init__(self):
        # User list, name, and versions. All inherent settings.
        self.users = []
        self.name = "Serpens Vivus"
        self.error = []
        self.recently_deleted_users = []
        self.utilities = ["Settings", "System Info", "Notepad", "SpeedSlow"]
        self.games = ["Bagels", "Tictactoe", "Hangman ", "Sonar", "Joke Teller", "ScoutRPG"]
        self.admin = ["Reset", "Event Viewer", "Task Manager"]
        self.versions = {"Main": "4.0beta02", "Bagels": 4.5, "Event Viewer": 1.1, "Hangman": 3.5,
                         "Joke Teller": 2.4, "Notepad": 2.2, "ScoutRPG": "alpha1.6",
                         "Sonar": 2.1, "SpeedUpOrSlowDown": 1.2, "Sudoku": 1.0, "System Info": 1.6,
                         "System Recovery": 1.3, "Tictactoe": 5.7,
                         "Settings": "1.0beta01"}
        self.path = "Users\\{}"
        self.current_user = User()
        Loading.log("Boot complete.")
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.name + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
            self.current_user.username + "\n Current Password is hidden. >"

    # noinspection PyUnreachableCode
    def reload(self):
        """
        This method reloads the OS variables from the disk. Very useful in a restart because one does not have to close the
        python shell.
        :return:
        """
        self.error = []
        new_users = []
        for subdir, dirs, files in os.walk("Users"):
            if len(dirs) == 0 and len(files) == 0:
                self.setup()
                return
            if "info.usr" in files:
                user_file = list(open("{}\\info.usr".format(subdir), 'r'))
                info = Loading.caesar_decrypt(user_file[0]).split('\n')[0].split(user_separator)  # UserType, Username, Password, Current Status, Color (if applicable)
                programs = Loading.caesar_decrypt(user_file[1]).split('\n')[0].split(program_separator)
                if 4 <= len(info) <= 5:
                    try:
                        new_users.append(globals()[info[0]](info[1], info[2], info[3] == "True", programs, (info[4].split(personalization_separator) if len(info) == 5 else None), self.path.format(info[1])))
                    except (AttributeError, IndexError, KeyError):
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
            if self.current_user.username == "Default" and self.current_user.password == "Default" and self.current_user.__class__.__name__ == "User":
                self.error.append(system_recovery.NoCurrentUser())
            if not admin_present:
                self.error.append(system_recovery.NoAdministrator())
            if self.error:
                raise Exception((self.error[0].__repr__() if len(self.error == 1) else "Multiple fatal errors occurred.") + " Please reboot the system.")
            return
        else:
            self.setup()
            return

    def startup(self):
        """
        This method regulates the startup and login of the OS. Allows to shut down and switch users.
        :return: Shutdown values returned from operating_system().
        """
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
            try:
                print("\033[{}m".format(self.current_user.color), end='')
                Loading.SPEED = self.current_user.speed
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
                        pwd = maskpass.advpass(prompt="Enter password.\n", ide=True)
                        if pwd == self.current_user.password:
                            Loading.returning("Welcome!", 1)
                            # Move to the system screen.
                            os_rv = self.operating_system()
                            Loading.log("Code {} returned. Executing task.".format(os_rv))
                            # Logic for returning from the OS screen.
                            if os_rv == 1:
                                input("{}The System is sleeping. Press [ENTER] or [return] to wake.".format("\n" * 10))
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
                                input("{}The System is sleeping. Press [ENTER] or [return] to wake.".format("\n" * 10))
                                break
                            elif shutdown == 0:
                                pass
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
                        print("WARNING: The Guest account will boot into the main screen, but any user settings or games will have no effect. \nThis includes usernames, passwords, game progress, saved notes, etc.")
                        print("All games will say that the file or path is not found, this is normal. The Guest User doesn't have a user folder.\nPress [ENTER] or [return] to login.")
                        if input() == 'debugexit':
                            return
                        Loading.log("Guest user logged in")
                        self.operating_system()
                        return 3
            except Loading.LockInterrupt as lock:
                Loading.returning("Locking Computer...", 1)
                if lock.args[0] and lock.args[0].__class__ not in [k.__class__ for k in self.current_user.saved_state]:
                    self.current_user.saved_state.append(lock)
                pass

    def operating_system(self):
        """
        Method operating_system(). The home screen and hub for almost every command in the OS.
        :return:
        """
        # The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
        Loading.log(self.current_user.username + " logged in.")
        while True:
            try:
                if [i for i in self.current_user.saved_state if i.__class__.__name__ == "LockInterrupt"]:
                    swap = [i for i in self.current_user.saved_state if i.__class__.__name__ == "LockInterrupt"][0]
                    self.current_user.saved_state.remove(swap)
                    swap.args[0].main()
                print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                # Main while loop for applications.
                max_len = [len(max(self.utilities, key=len)), len(max(self.games, key=len))]
                margin = [(int(i / 8) + (2 if i % 8 else 1)) * 8 for i in max_len]
                print(("\nAPPLICATIONS\n{underline}UTILITIES{clear}{util}{underline}GAMES{clear}" + ("{games}{underline}ADMIN{clear}" if self.current_user.elevated else "") +
                       "{clear}").format(underline="\033[4m", clear="\033[0;{}m".format(self.current_user.color), util=" " * (margin[0] - 9), games=" " * (margin[1] - 5)))
                for i in range(len(max(self.utilities, self.games, self.admin, key=len))):
                    print((self.utilities[i] if i < len(self.utilities) else "") + " " * (margin[0] - (len(self.utilities[i]) if i < len(self.utilities) else 0)), end="")
                    print((self.games[i] if i < len(self.games) else "") + " " * (margin[1] - (len(self.games[i]) if i < len(self.games) else 0)), end="")
                    if self.current_user.elevated:
                        print(self.admin[i] if i < len(self.admin) else "")
                    else:
                        print()
                print("\nLock Computer\tPower".expandtabs(8))
                choice = input().lower()
                # This logs what app the user opened, but the number codes still work.
                Loading.log(self.current_user.username + " opened " + choice)
                choices_list = {Jokes: ('jokes', 'joke', '1', 'joke teller'), Notepad: ('notepad', 'notes', 'note', '2')
                                , SpeedUpOrSlowDown: ('speedslow', 'speed up', 'slow down', 'speed up or slow down')
                                , Bagels: ('bagels', 'bagels', '3'), Tictactoe: ('tictactoe', 'tic-tac-toe', 'ttt', '4')
                                , Hangman: ('hangman', '5'), Sonar: ('sonar', '6'), ScoutRpg: ("scout rpg", "scout", "rpg", "scout_rpg", "scoutrpg")
                                , Settings: ('settings', '8'), SystemInfo: ('system info', 'sys info', '9')
                                , TaskManager: ('task manager', '7'), EventViewer: ('event viewer', 'events'), Reset: ('reset', '10')}
                if choice in ('exit', 'lock computer', 'lock', '11'):
                    Loading.log(self.current_user.username + " logged out.")
                    print("Computer has been locked.")
                    return 'regular'
                elif choice in ('shutdown', '12', 'power'):
                    Loading.log(self.current_user.username + " logged out and shutdown.")
                    code = self.shutdown()
                    if code == 0:
                        pass
                    else:
                        return code
                elif choice in ('debugexit', 'debug'):
                    return 'regular'
                for j in choices_list:
                    if choice in choices_list[j]:
                        # self.current_user.saved_state[j] = True
                        if j in [k.args[0].__class__ for k in self.current_user.saved_state]:
                            swap = [k for k in self.current_user.saved_state if k.args[0].__class__ == j][0]
                            self.current_user.saved_state.remove(swap)
                            swap.args[0].main()
                            break
                        if list(choices_list.keys()).index(j) >= len(choices_list) - 3:
                            if self.current_user.elevated:
                                if j.boot(self) == 4:
                                    return 4
                        else:
                            if j.category == "games":
                                if j.boot(self.path.format(self.current_user.username)) == 'regular':
                                    print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                                    return 'regular'
                            elif j.category == "utilities":
                                if j.boot(self) == 'regular':
                                    print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                                    return 'regular'
                            else:
                                raise Exception(
                                    "The Application has an incorrect category.")
                        break
                else:
                    Loading.returning("Please choose from the list of applications.", 1)
            except Loading.HomeInterrupt as home:
                if home.args[0]:
                    self.current_user.saved_state.append(home)
                pass
            except Exception as app_error:
                if not OperatingSystem.HANDLE_ERROR:
                    raise app_error
                input("The application has encountered a fatal error and has crashed.\nThis could be a result of a corrupted save file, or a damaged application. Try running System Recovery.")
                pass

    def shutdown(self):
        """
        Method shutdown(). Handles sleeping, hibernating, shutting down, and restarting properly and modifies user files accordingly.
        :return:
        """
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
            if shutdown_choice == "":
                return 0
            elif shutdown_choice == "info":
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
                                program_count += 1
                            else:
                                i.saved_state.remove(j)
                    if program_count > 0:
                        if input('Programs are running. Would you like to force quit them? All progress will be lost. '
                                 'Type "yes" or "no".').lower() not in ("yes", "y", "of course", "absolutely"):
                            return 0
                        print("Waiting for {} {} to close.".format(program_count, "programs" if program_count > 0 else "program"))
                        for _ in range(len(self.current_user.saved_state)):
                            Loading.returning("Closing {}.".format(str(self.current_user.saved_state[0].__class__.__name__)), 2)
                            self.current_user.saved_state.pop(0)
                        if shutdown_choice in ('shutdown', '3'):
                            print("Shutting down...")
                        else:
                            print("Restarting...")
                        Loading.log("All apps closed.")
                    else:
                        print("No apps are open.")
                # Now write each user's info to their respective info files.
                for i in self.users:
                    # Open their file, write encrypted data and close the file.
                    Loading.log("Updating user files...")
                    user_file = open(self.path.format(i.username) + "\\info.usr", 'w')
                    user_file.write(Loading.caesar_encrypt(i.__repr__()))
                    # user_file.write(Loading.caesar_encrypt(i.__class__.__name__ + '(U)' + i.username + '(U)' + i.password + "(U)" + str(i.current) + '(U)\n'))
                    # user_file.write(Loading.caesar_encrypt("(P)".join(j.__repr__() for j in i.saved_state) + '\n'))
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
        """
        Method setup(). This method sets the system up with the correct files. Soon to be overhauled to download files from GitHub.
        :return:
        """
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
            self.current_user = Administrator(setup_user, setup_pwd)
            Loading.returning("Password set successfully.", 2)
            Loading.returning("One last thing!", 1)
            recovery_pwd = ''.join(str(random.choice(Loading.ALPHABET)) for _ in range(1000)) + '(R)' + input("Please enter a recovery password.") + '(R)' + ''.join(str(random.choice(Loading.ALPHABET)) for _ in range(1000))
            recovery_file = open("System\\recovery.info", 'w')
            recovery_file.write(Loading.caesar_encrypt(recovery_pwd))
            recovery_file.close()
            self.users.append(self.current_user)
            os.mkdir(self.path.format(self.current_user.username))
            user_file = open(self.path.format(self.current_user.username) + "\\info.usr", 'w')
            user_file.write(Loading.caesar_encrypt(self.current_user.__class__.__name__ + '(R)' + self.current_user.username + '(R)' + self.current_user.password + "(R)" + str(self.current_user.current) + '(R)\n\n'))
            user_file.close()
            Loading.returning("Entering startup in 3 seconds.", 3)
        else:
            # If the user did not specify whether they wanted a new user.
            self.current_user = Administrator("Guest", "")
            self.users.append(self.current_user)
            Loading.returning("Guest user added. There is no password. Entering startup in 3 seconds.", 3)
            os.rmdir("Users")
        Loading.log("SETUP is complete. Entering startup.")
        return
