"""
Module operating_system. This module contains the Core Python OS functions and classes. Probably the most complex file in the system.
"""
import io
import colorama
import traceback
import importlib
import os
import time
import requests

try:  # Try importing all the files.
    from System import Loading, Registry, recovery, User

    apps = {"games": [], "utilities": [], "admin": []}
    for file in [files for subdir, dirs, files in os.walk("Applications")][0]:
        temp = (importlib.import_module("Applications.{}".format(file.replace(".py", ""))))
        temp.__setattr__("__name__", file.replace(".py", ""))
        apps[temp.category].append(temp)
except ImportError as missing_files:  # If any of the files fail to import, they are assumed missing.
    # Trying a download algorithm that seemingly doesn't need an auth token.
    Loading = Registry = recovery = User = None
    # noinspection PyUnresolvedReferences
    files = {missing_files.name_from, "Loading", "Registry", "recovery", "User"}
    print("The system is missing files. Attempting re-download from GitHub.")
    for filename in files:
        try:
            new_file = requests.get("https://raw.githubusercontent.com/Cerberus1470/Serpens-Vivus/Tejas/System/{file}.py".format(file=filename))
            if new_file.status_code == 200:  # Checking for 200 OK Response Code
                with open("System\\{file}.py".format(file=filename), 'w') as file:
                    file.write(new_file.text)
        except (io.UnsupportedOperation, OSError, FileNotFoundError, FileExistsError):
            print("The system was unable to write to System\\{file}.py. Please download it from GitHub.".format(file=filename))
    raise ImportError("The system was missing files. Please reboot the system.")


def find_app(target : str = "FileEngine"):
    """
    Helper method to get a specific app from the applications list.
    :param target: The app to find. Is a string, and default is the FileEngine.
    :return: The list of apps, regardless of category.
    :raises: IndexError if the target class is not found.
    """
    apps_modules = [app for category in apps.values() for app in category] + [Loading, Registry, recovery, User]  # First make the total apps list.
    apps_classes = {j for i in apps_modules for j in i.__dict__.values() if type(j) == type}  # Then gather all classes. Remove duplicates by using a set.
    if target == "_all": return apps_modules+list(apps_classes)
    return [i for i in apps_modules+list(apps_classes) if i.__name__ == target][0]  # Access Control to make sure user KNOWS the class name.


# Public Variables
user_separator = "(U)"
program_separator = "(P)"
personalization_separator = "(Pe)"
HANDLE_ERROR = True
version = "4.1"


# noinspection PyBroadException
def boot(error=True, stacktrace=False):
    """
    Method boot(). This method regulates the boot process of the Core OS. It is responsible for allowing one-line startup.
    :return: 0 if no crashes occur. Code 1-5 if an error occurs.
    """
    # Some extra methods to set variables
    global HANDLE_ERROR
    HANDLE_ERROR = error
    colorama.just_fix_windows_console()
    start = time.time()
    cerberus = OperatingSystem()  # Initialize OS Object.
    Loading.log("System Startup.")
    while True:
        try:
            if cerberus.error:  # This code catches any boot errors.
                recovery.boot(cerberus.error)
            cerberus.reload()
            if cerberus.startup() == 4:  # Logic for restarting.
                Loading.returning("Restarting system...", 2)
                Loading.returning("Booting...", 2)
            else:
                return "Code 0. Execution successful."
        # Screen for fatal errors. Catches all exceptions and prints the stacktrace. Reboots automatically.
        except Exception as fatal_error:
            if not HANDLE_ERROR:
                raise fatal_error
            Loading.log("{name} encountered a fatal error: {error}".format(name=cerberus.name, error=fatal_error if stacktrace else "Stacktrace disabled"))
            print('{new_line}{msg}{stacktrace}\n'.format(
                new_line='\n' * 20, msg="!!! {name} encountered a fatal error. Reboot is required. !!!".format(name=cerberus.name),
                stacktrace=("\nWhat failed: {file}\n\nStacktrace: \n{trace}".format(file=str(traceback.__file__), trace=str(traceback.format_exc()))) if stacktrace else ""))
            Loading.returning("The system will reboot shortly.", 5)
            continue
            # return "Code {}. A system error has occurred.".format(','.join([str(i.code) for i in cerberus.error]) if cerberus.error else "-1")
        Loading.log("System Shutdown. {} seconds have elapsed.".format(str(time.time() - start)))
    return


# noinspection PyBroadException
class OperatingSystem:
    """
    Class Operating System. Houses all the core functions aside from boot.
    """

    def __init__(self, users=None, name=None, error=None, rdu=None, path=None, reg=None, cu=None):
        # User list, name, and version. All inherent settings.
        self.users = [] if not users else users
        self.name = "Serpens Vivus" if not name else name
        self.error = [] if not error else error
        self.recently_deleted_users = [] if not rdu else rdu
        self.path = "Users\\{}" if not path else path
        self.registry = Registry.Registry("System\\REGISTRY", self.elevate) if not reg else reg
        self.current_user = User.User() if not cu else cu
        Loading.log("Boot complete.")
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named {name}\n Users: {users}\n Current User: {current}\n Current Password is hidden. >" \
            .format(name=self.name, users=str(len(self.users)), current=self.current_user.username)

    def copy(self):
        """
        Method to return a copy of the OS
        :return:
        """
        return OperatingSystem(self.users.copy(), self.name, self.error.copy(), self.recently_deleted_users.copy(), self.path,
                               Registry.Registry("SYSTEM\\REGISTRY"), self.current_user.copy(self.path.format(self.current_user.username)))

    # noinspection PyUnresolvedReferences
    def reload(self):
        """
        This method reloads the OS variables from the disk. Very useful in a restart because one does not have to close the
        python shell.
        :return:
        """
        self.error.clear()  # Reset errors and users.
        self.users.clear()
        for subdir, dirs, files in os.walk("Users"):
            if len(dirs) == 0 and len(files) == 0:  # If no users exist (or there is no user folder)
                self.setup()
                return
            info = person = programs = None
            try:
                if "info.usr" in files:
                    user_file = Loading.caesar_decrypt(''.join(list(open("{}\\info.usr".format(subdir), 'r'))), priority=2).split('\n')
                    info = user_file[0].split(user_separator)  # UserType, Username, Password, Current Status
                    person = user_file[1].split(personalization_separator)  # Color, Background, Taskbar list
                    programs = user_file[2].split(program_separator)
                    if len(info) == 4 and len(person) == 3:
                        self.users.append(User.__getattribute__(info[0])(username=info[1:], saved_state=programs, personalization=person, path=self.path.format(info[1])))  # Try creating the user object.
                    else:
                        raise AttributeError
            except (IndexError, TypeError, AttributeError):
                self.error.append(recovery.CorruptedFileSystem(subdir, info, person, programs))
        if self.users or self.error:  # Begin the error detection!
            self.current_user = [i for i in self.users if i.current]
            admin_present = bool([i for i in self.users if i.elevated])
            self.current_user = self.current_user[0] if len(self.current_user) == 1 else self.users[0]
            if not admin_present:
                self.error.append(recovery.NoAdministrator())
            if self.error:
                raise self.error[0] if len(self.error) == 1 else Exception("Multiple fatal errors occurred.")
            # Now we can verify the registry has the required keys.
            if self.registry.verify_build(["Resolution", "Recovery", "Speed"] + ["SVKEY_USER\\{user}\\Start".format(user=i.username.upper()) for i in self.users]):
                Loading.SPEED = float(self.registry.get_key("Speed"))
            else:
                raise recovery.CorruptedRegistry(self.registry)
        else:
            self.setup()
            return

    def elevate(self) -> bool:
        """
        Universal method to elevate user privileges for a specific purpose. Use in a boolean expression for any protected action.
        :return: True if elevation succeeded, False if it did not.
        """
        print("The requested action requires administrator privileges.")
        user = self.current_user
        if not self.current_user.elevated:  # If the current user is standard, prompt for an admin name.
            uname = input("Please enter an administrator's username: ")
            try:
                user = [i for i in self.users if i.username.lower() == uname.lower()][0]
                if not user.elevated:
                    Loading.returning("That user is not an administrator.", 2)
                    return False
            except IndexError:  # Invalid user, not in user list.
                Loading.returning("That is not a valid user.", 2)
                return False
        pwd = Loading.pass_input("Enter administrator password: ", mask='-')
        if user.password == pwd:
            return True
        else:
            Loading.returning("That password is not correct.", 2)
            return False

    def startup(self) -> int:
        """
        This method regulates the startup and login of the OS. Allows to shut down and switch users.
        :return: Shutdown values returned from operating_system().
        """
        while True:  # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
            try:
                print(Loading.colored("\nHello! I am {name}".format(name=self.name), self.current_user.color))
                for i in range(3):
                    print('\nCurrent User: {c_user}. Type "switch" to switch users or "power" to open the power menu.'.format(c_user=self.current_user.username))
                    pwd = Loading.pass_input()
                    if pwd == self.current_user.password:
                        Loading.returning("Welcome!", 1)
                        Loading.log("User {user} logged in.".format(user=self.current_user.username))
                        os_rv = self.operating_system()  # Move to the system screen.
                        Loading.log("Code {} returned. Executing task.".format(os_rv))
                        match os_rv:  # Logic for returning from the OS screen.
                            case 0 | 1:
                                break
                            case _:
                                return os_rv
                    elif pwd == 'switch':  # Switch users!
                        self.switch_user()
                        break
                    elif pwd in ('shutdown', 'power'):  # Shutting down...
                        shutdown = self.shutdown()
                        match shutdown:
                            case 0 | 1:
                                break
                            case _:
                                return shutdown
                    elif pwd == 'debugexit':  # Carryover from original code :)
                        Loading.log("Code debug returned.")
                        return 'debug'
                    else:
                        Loading.returning("Sorry, that's the wrong password. Try again.", 2)
                        continue
                else:
                    Loading.returning("You have incorrectly entered the password 3 times. The computer will now restart.", 5)
                    return 4
            except Loading.LockInterrupt as lock:
                Loading.returning("Locking Computer...", 1)
                if lock.args[0] and lock.args[0].__class__ not in [k.__class__ for k in self.current_user.saved_state]:
                    self.current_user.saved_state.append(lock)

    def operating_system(self):
        """
        Method operating_system(). The home screen and hub for almost every command in the OS.
        :return: 0 for locking, 1 for sleep, 2 for hibernate, 3 for shutdown, 4 for restart.
        """
        # The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
        while True:
            try:
                if Loading.LockInterrupt in [i.__class__ for i in self.current_user.saved_state]:  # If any game was stopped by locking
                    self.current_user.saved_state.pop(-1).args[0].main()
                print("\nHello! I am {name}, running POCS v{version}".format(name=self.name, version=version))  # Print the welcome message, the user's background, and the taskbar.
                [print(i, end='') for i in list(open("System\\bg\\{res}\\{bg}".format(res=self.registry.get_key("Resolution"), bg=self.current_user.background)))]
                print("\nSV |  {taskbar}".format(taskbar="  ".join(self.current_user.taskbar)))
                print('\nWelcome to {name}! This is the main desktop.\nType "sv" or "start" to open the apps screen, or type the name of an app in the taskbar to open that.\n'.format(name=self.name))
                choice = input().lower()  # Desktop input
                if choice in ('sv', 'start', 'apps'):  # If the user opens the apps menu.
                    match self.registry.get_key("SVKEY_USER\\{}\\Start".format(self.current_user.username.upper())):  # Alphabetical or categorized sorting?
                        case 'alphabetical':
                            names = sorted([i.__name__.replace("_", " ").title() for i in apps.values() for i in i])
                            apps_display = [names[i:i + 5] for i in range(0, len(names), 5)]
                            max_len = [-(-max([len(j) for j in i]) // 5) * 5 for i in apps_display]
                        case 'categorized':
                            apps_display = [sorted([j.__name__.replace("_", " ").title() for j in apps[i]]) for i in apps]
                            max_len = [-(-max([len(j) for j in i]) // 5) * 5 for i in apps_display]
                        case _:
                            raise recovery.CorruptedRegistry(self.registry)  # If the sort isn't recognized.
                    for i in range(5):  # Print the apps screen.
                        for j in range(3):
                            try:
                                print("{app}{space}\t".format(app=apps_display[j][i], space=' ' * (max_len[j] - len(apps_display[j][i]))), end='\n' if j % 3 == 2 else '')
                            except IndexError:
                                print()
                                break
                    choice = "sv_" + input().lower()  # Apps menu input
                choices_list = {j: j.entries for j in apps.values() for j in j}  # Create the list of choices. Number codes still work!
                Loading.log("{user} opened {choice}".format(user=self.current_user.username, choice=choice))  # This logs what app the user opened
                if not choice or choice in ('exit', 'lock computer', 'lock', '11'):
                    Loading.log("{} logged out.".format(self.current_user.username))
                    print("Computer has been locked.")
                    return 0
                elif choice in ('shutdown', '12', 'power'):
                    code = self.shutdown()
                    if code:
                        Loading.log("{user} exited the shutdown with code {code}".format(user=self.current_user.username, code=code))
                        return code
                elif choice in ('debugexit', 'debug'):
                    return 0
                else:
                    for i in choices_list:  # Now iterate! If the choice is alone and in the taskbar, or if it was selected through the apps menu, run the boot().
                        if (choice in choices_list[i] and choice in [i.lower() for i in self.current_user.taskbar]) or ("sv_" in choice and choice.replace("sv_", "") in choices_list[i]):
                            for j in range(len(self.current_user.saved_state)):  # Checking for HomeInterrupts
                                # noinspection PyUnresolvedReferences
                                if choice in find_app(self.current_user.saved_state[j].args[0].__module__.partition('.')[2]).entries:
                                    self.current_user.saved_state.pop(j).args[0].main()
                            i.boot(self)
                            break
                    else:  # If the for loop was exhausted (not a valid choice).
                        Loading.returning("Please choose a valid option.", 2)
            except Loading.HomeInterrupt as home:
                if home.args[0]:
                    self.current_user.saved_state.append(home)
            except Loading.LockInterrupt as lock:
                if lock.args[0]:
                    raise lock
            except Exception as app_error:
                if not HANDLE_ERROR:
                    raise app_error
                Loading.returning("The application has encountered a fatal error and has crashed.\nThis could be a result of a corrupted save file, or a damaged application. Try running System Recovery.", 5)

    def shutdown(self):
        """
        Method shutdown(). Handles sleeping, hibernating, shutting down, and restarting properly and modifies user files accordingly.
        :return: 0 for exit, 1 for sleep, 2 for hibernate, 3 for shutdown, 4 for restart.
        """
        Loading.log("Preparing to shut down...")  # The shutdown method. Saves everything to disk and rides return statements all the way back to the main file. Exits safely after that.
        hibernate = shutdown = restart = False
        if self.current_user.username == 'Guest':
            Loading.returning("You have logged in as a guest user. Guest user details are not stored to the disk.")
            if input("Would you like to save the guest user under a different name?") in ('yes', 'y', 'of course', 'absolutely'):
                while True:
                    new_uname = input("What should the new user be named? Alphanumeric, case-sensitive, no escape characters.")
                    if "\\" in new_uname:  # Making sure escape characters aren't present.
                        Loading.returning("Escape characters are not supported.", 2)
                    elif new_uname == "Default" or new_uname in [i.username for i in self.users]:  # Avoiding users with the same name.
                        Loading.returning("That username is taken.", 2)
                    else:
                        self.current_user.username = new_uname
                        os.rename("Users\\Guest", "Users\\{}".format(self.current_user.username))
                        shutdown = True
                        break
        while True:
            # While loop to choose what type of shutdown to do.
            match input("Choose an option.\n1. Sleep\n2. Hibernate\n3. Shutdown\n4. Restart\nType \"info\" for details.").lower() if not shutdown else "shutdown":
                case "":  # No input
                    return 0
                case "info" | "help":  # Help!
                    print("1. Sleep\nSleep does not close the python shell. It logs out the current user and saves the session to RAM. Forcibly closing "
                          "the shell will result in lost data.\n2. Hibernate\nHibernate saves the current session to disk and exits the python shell. "
                          "The python shell is closed and all data is saved.\n3. Shutdown\nShutdown saves only users and notes to disk. All other data "
                          "is erased and all apps are quit.\n4. Restart\nRestart shuts down the computer, saving only users and notes to disk, and opens "
                          "the program again.")
                    Loading.returning(length=10)
                    continue
                case "sleep" | "1":  # Return sleep code.
                    print("Sleeping...{}The System is sleeping. Press [ENTER] or [return] to wake.".format("\n" * 10))
                    return 1
                case "hibernate" | "2":
                    print("Hibernating...")
                    hibernate = True
                case "shutdown" | "3":
                    print("Shutting down...")
                    shutdown = True
                case "restart" | "4":
                    print("Restarting...")
                    shutdown = restart = True
                case _:
                    Loading.returning("Please choose a valid option.", 2)
                    continue
            if self.current_user.saved_state and (shutdown or restart):  # If there are running apps.
                if input('Programs are running. Would you like to force quit them? All progress will be lost.').lower() in ("yes", "y", "of course", "absolutely"):
                    Loading.log("Closing apps.")
                    print("Waiting for {num} {txt} to close...".format(num=len(self.current_user.saved_state), txt=('programs' if len(self.current_user.saved_state) == 2 else 'program')))
                    [Loading.returning("Closing {}...".format(i.args[0].__class__.__name__), 2) for i in self.current_user.saved_state]
                    [i.saved_state.clear() for i in self.users]
                    Loading.log("All apps closed.")
                else:
                    return 0
                print("Shutting down..." if shutdown else "Restarting...")
            Loading.log("Updating user files...")
            for i in self.users:  # Now write each user's info to their respective info files.
                with open(self.path.format(i.username) + "\\info.usr", 'w') as user_file: # Open their file, write encrypted data and close the file.
                    user_file.write(Loading.caesar_encrypt(i.__repr__(), priority=2))  # Using the repr() for each user, containing everything!
            Loading.log("User files updated.")  # Finishing with some print statements.
            if restart:
                return 4
            input("{word} complete. Open {name}.py to restart the system.".format(word="Hibernation" if hibernate else "Shutdown", name=self.name))
            return 2 if hibernate else 3

    def switch_user(self):
        """
        Sub-program to switch the current user.
        :param self: The OS Object to get info from.
        :return: Nothing.
        """
        if len(self.users) <= 1:
            Loading.returning("There is only one user registered.", 2)
            return
        print("Current User: {}".format(self.current_user.username))
        print('\n'.join(["{num}. {app}".format(num=self.users.index(i) + 1, app=i.username.title()) for i in self.users]))
        while True:
            user_selection = input("Choose a user.\n")
            if user_selection.lower() == 'exit':
                return
            if user_selection in [i.username for i in self.users]:
                self.current_user.current = False
                self.current_user = [i for i in self.users if i.username == user_selection][0]
                self.current_user.current = True
                Loading.returning("Returning to the login screen in 3 seconds.", 3)
                return
            else:
                Loading.returning('Please choose a user from the list or type "exit" to exit.', 2)

    def setup(self):
        """
        Method setup(). This method sets the system up with the correct files. Soon to be overhauled to download files from GitHub.
        :return: Nothing
        """
        # The setup method. Conveniently sets up the system to run on its first boot, and whenever there is no data. Modifies the dictionary with a new user.
        Loading.log("The system has entered SETUP.")
        os.makedirs(self.path.format(""), exist_ok=True)  # Make the user folder (if it doesn't already exist).
        guest = False  # Flag for guest users.
        if input("SETUP: Since this is the first time you're running this OS, you have entered the setup.\n"
                 "Would you like to create a new user, or login as guest?\n") not in ('new user', 'new', 'user', 'yes'):  # Then ask the user if they want to make a user or not.
            guest = True
        while True:  # Quick username validation.
            setup_user = input("Name your user:\n") if not guest else "Guest"  # New username
            if "\\" not in setup_user:  # Quick check for validity.
                break
            Loading.returning("Escape characters are not supported.", 2)
        print("New User added. Enter a password or press [ENTER] or [return] to use the default password." if not guest else "Guest User added.")
        while True:  # The while loop handles the password creation. Can only escape under certain circumstances.
            setup_pwd = input() if not guest else ""
            if setup_pwd:  # If the user entered a password:
                if setup_pwd == (input("Password set. Enter it again to confirm it.") if not guest else ""):
                    Loading.returning("Password set.", 2)
                    break
                else:  # Handle password matching. Loops back to ensure the user typed the correct passwords.
                    Loading.returning("The passwords you entered didn't match. Type the same password twice.", 2)
            else:  # If the user did not enter a password.
                setup_pwd = "python123"
                Loading.returning('Default password set. The password is "python123".', 2)
                break
        # User entered password correctly twice.
        self.current_user = User.Administrator(setup_user, setup_pwd)  # Create the user object
        self.users.append(self.current_user)  # Add the user and save it to disk.
        os.mkdir(self.path.format(self.current_user.username))
        with open(self.path.format(self.current_user.username) + "\\info.usr", 'w') as user_file:
            user_file.write(Loading.caesar_encrypt(self.current_user.__repr__()))
        Loading.returning("One last thing!" if not guest else "", 1 if not guest else 0)  # Ask for a recovery pwd if not a guest.
        recovery_pwd = input("Please enter a recovery password.") if not guest else "guest"
        self.registry.set_svkey("Recovery", Loading.caesar_encrypt(recovery_pwd))  # Modify the registry.
        Loading.returning("Entering startup in 3 seconds.", 3)
