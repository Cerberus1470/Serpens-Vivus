"""
Program full of nothing at the moment.
"""
import io
import requests
import os
from System import Loading, User, operating_system

category = "utilities"
version = "1.3"
entries = ('settings', '8')


# The object passed by the OS will always be the os_object. If it's not, someone else is calling the method.
def boot(os_object=None):
    """
    This method regulates the startup process for this application.
    :param os_object: The OS Object, used to obtain the current user's text color.
    :return: Nothing
    """
    settings = Settings(os_object)
    settings.main()


class Settings:
    """
    Main class to house everything!
    """

    def __init__(self, os_object: None = None):
        self.os_object = os_object
        self.entries = {"Personalize": ("Edit Text Color", "Edit Background", "Change Taskbar"),
                        "System": ("Resolution", "Speed"),
                        "Users": ("Add New User", "Edit Username", "Edit Password", "Delete User", "Restore User", "Switch User"),
                        "Updates": ("Check for Updates", "Update History"),
                        "Recovery": ("Verify OS Integrity", "Back Up Files", "Reset")}
        return

    def __repr__(self):
        return

    @staticmethod
    def settings_menu(title: str = "TITLE", dictionary: dict = None, selected_category: str = "", color: int = 0):
        """
        A universal method to print out a "graphical" menu with provided materials.
        :param title: The title to display at the top of the menu.
        :param dictionary: The dictionary provided.
        :param selected_category: The selected category from which to display options.
        :param color: The color for formatting the text to.
        :return: Nothing. This method is meant to print everything by itself.
        """
        if not dictionary:
            print("The dictionary is empty.")
            return
        max_len = len(max(dictionary.keys(), key=len))
        margin = (int(max_len / 8) + (2 if max_len % 8 else 1)) * 8
        print("{}{}|        \033[4m{}\033[0;{}m\n{}|".format("\033[4m{}\033[0;{}m".format(title, color) if not selected_category else title, " " * (margin - len(title)), selected_category.upper(), color, " " * margin))
        s = 0
        for i, v in enumerate(list(dictionary.keys())):
            print("\033[4m{category}\033[0;{}m".format(color, category=v) if v == selected_category else v, end=" " * (margin - len(v)) + "|")
            if selected_category:
                try:
                    print("        {}".format(dictionary[selected_category][s]), end="")
                    print("\n{}|        {}".format(" " * margin, dictionary[selected_category][s + 1]), end="")
                except IndexError:
                    print("\n{}|".format(" " * margin), end="")
                finally:
                    print()
                s += 2
            else:
                print("\n{}|".format(" " * margin))
            continue
        return

    def main(self):
        """
        The main method for all the settings.
        :return: Nothing.
        """
        print("Welcome to Settings!\nThis is the universal settings app to customize anything.\nChoose a category.\n")
        while True:
            Settings.settings_menu("SETTINGS", self.entries, color=self.os_object.current_user.color)
            choice = Loading.pocs_input()
            match choice.lower():
                case "personalize" | "person" | "per":
                    self.personalize()
                case "system" | "sys":
                    self.system()
                case "users" | "user" | "user settings":
                    self.users()
                case "updates" | "update" | "upgrades" | "upgrade":
                    self.updates()
                case "recovery" | "recover" | "restore" | "restoration":
                    self.recovery()
                case "" | "exit" | "let me leave":
                    break
                case _:
                    Loading.returning("Please choose from the list of choices.", 2)
        return

    def personalize(self):
        """
        Method for the Personalize Settings Sub-menu.
        :return: Nothing.
        """
        while True:
            Settings.settings_menu("SETTINGS", self.entries, "Personalize", self.os_object.current_user.color)
            match input().lower():
                case "edit text color" | "text" | "color" | "edit text" | "edit color" | "text color":
                    new_color = input("What would you like your text color to be? Current Color: {!s}\n".format(self.os_object.current_user.color))
                    if new_color in list(Loading.COLORS.keys()):
                        self.os_object.current_user.color = Loading.COLORS[new_color]
                    elif new_color in list(Loading.COLORS.values()):
                        self.os_object.current_user.color = new_color
                    else:
                        Loading.returning("That is not a valid color.", 5)
                        print("Here is a list of valid colors:\n{}".format("\n".join([i for i in list(Loading.COLORS.keys())])))
                        continue
                    Loading.returning(Loading.colored("Color set successfully!", self.os_object.current_user.color), 2)
                case "edit background" | "background" | "edit bg" | "bg":
                    print('\n'.join("{}. {}".format(i + 1, v) for i, v in enumerate(Loading.BACKGROUNDS)))
                    new_bg = input("Which background would you like? Current Background: {!s}\n".format(self.os_object.current_user.background))
                    if new_bg in [i.split('.')[0] for i in Loading.BACKGROUNDS] or new_bg in Loading.BACKGROUNDS:
                        self.os_object.current_user.background = new_bg + (".bg" if ".bg" not in new_bg else "")
                    else:
                        Loading.returning("That is not a valid background.", 2)
                        continue
                    Loading.returning("Background set up successfully!", 2)
                case "change taskbar" | "taskbar" | "change tb" | "tb":
                    print('\n'.join("{}: {}".format(i.title(), ', '.join(j.__name__.replace("_", " ").title() for j in operating_system.apps[i])) for i in operating_system.apps))
                    new_items = input("\nWhat apps do you want to add to your taskbar?\nEnter a single name, or a comma-separated list of names")
                    module_names = sorted([i.__name__ for i in operating_system.apps.values() for i in i])
                    if len(new_items.split(",")) >= 1 and all(i.lower().replace(" ", "_") in module_names for i in new_items.split(',')):  # Check both without space
                        self.os_object.current_user.taskbar.extend(new_items.split(","))
                    elif len(new_items.split(", ")) >= 1 and all(i.lower().replace(" ", "_") in module_names for i in new_items.split(', ')):  # And with space.
                        self.os_object.current_user.taskbar.extend(new_items.split(", "))
                    else:
                        Loading.returning("The list was not formatted correctly.", 2)
                        continue
                    Loading.returning("New items added to Taskbar!", 2)
                case "reset_personalize":
                    self.os_object.current_user.color = 0
                    self.os_object.current_user.background = "pyidea.bg"
                    self.os_object.current_user.taskbar = ["Notepad", "Settings"]
                    Loading.returning(Loading.colored("Personalization reset successfully.", self.os_object.current_user.color), 2)
                    return
                case "" | "exit" | "please":
                    return
                case _:
                    Loading.returning("Please choose from the list of options.", 2)

    def system(self):
        """
        Method for the Systems sub-menu.
        :return: Nothing.
        """
        while True:
            Settings.settings_menu("SETTINGS", self.entries, "System", self.os_object.current_user.color)
            choice = input()
            match choice.lower():
                case "resolution" | "res" | "change resolution" | "change res":
                    print("The resolution mainly affects the home screen (wallpaper and taskbar).\n"
                          "Length of text lines can be adjusted using the terminal window size.\n"
                          "Supported Resolutions (columns x rows): 10x40, 20x80, 30x120, 40x160")
                    new_resolution = input("What should the new resolution be?\n")
                    match new_resolution.lower():
                        case "10x40" | "10 x 40" | "10 by 40" | "10 pixels by 40 pixels":
                            new_resolution = "10x40"
                        case "20x80" | "20 x 40" | "20 by 80" | "20 pixels by 80 pixels":
                            new_resolution = "20x80"
                        case "30x120" | "30 x 40" | "30 by 120" | "30 pixels by 120 pixels":
                            new_resolution = "30x120"
                        case "40x160" | "40 x 40" | "40 by 160" | "40 pixels by 160 pixels":
                            new_resolution = "40x160"
                        case _:
                            Loading.returning("That is not a valid resolution", 2)
                            continue
                    Loading.returning("Changing Resolution...", 2)
                    self.os_object.registry.set_svkey("Resolution", new_resolution)
                case "change animation speed" | "animation" | "speed" | "change animation" | "change speed" | "animation speed":
                    try:
                        new_anim_speed = float(input("What should the new animation speed be (i.e. 1 = 1x, 2 = 2x, 0.5 = 0.5x)? Current Factor: {!s}\n".format(Loading.SPEED)))
                        if new_anim_speed <= 0:
                            raise ValueError
                    except ValueError:
                        Loading.returning("That is not a valid speed factor.", 2)
                    else:
                        Loading.SPEED = new_anim_speed
                    pass
                case "" | "exit" | "please":
                    return
                case _:
                    Loading.returning("Please choose from the list of options.", 2)

    # noinspection PyUnresolvedReferences
    def users(self):
        """
        Method for the Users Settings Sub-menu. Built from the ground up based on the deprecated user_settings.py app.
        :return: Nothing.
        """

        def print_all_users(message: str = "Select a User.", access: int = 0) -> User:
            """
            Method to print a numbered list of all users currently registered. Allows selection of a valid user based on priority.
            :param message: Message to display when collecting input.
            :param access: Level of input privilege elevation. 0 means do not collect, 1 mean Standard Users, 2 means Admins and Standard.
            :return: The selected user.
            :raises: PermissionError if access level is not 0, 1, or 2.
            """
            print("\n".join(["{number!s}. {name!s}".format(number=i+1, name=self.os_object.users[i].username) for i in range(len(self.os_object.users))]))
            if access == 0:  # If priority is 0 (default), do not collect input.
                return
            elif access == 1 or access == 2:
                user_select_master = input(message)
                try:
                    user_select_master = [i for i in self.os_object.users if i.username == user_select_master][0]
                    if access == 1 and user_select_master.__class__ == User.Administrator and user_select_master != self.os_object.current_user:
                        Loading.returning("You do not have enough privileges to alter other administrators.", 2)
                    else:
                        return user_select_master
                except IndexError:
                    Loading.returning("That is not a valid username.", 2)
            else:  # If the access level is not 0, 1, or 2.
                raise PermissionError("That access level is not valid.")

        while True:  # The main while loop for users.
            Settings.settings_menu("SETTINGS", self.entries, "Users", self.os_object.current_user.color)
            choice = input()
            match choice.lower():
                case "add new user" | "add" | "new" | "add new" | "add user" | "new user":  # The add user wizard.
                    print("Welcome to the Add New User Wizard!")
                    if self.os_object.current_user.elevated:  # First check if the current user is an admin. Standard users cannot add users.
                        while True:  # In case they type "help".
                            new_user_type = input('What type should this user be?\n1. Standard User\n2. Administrator\nType "help" for help.')
                            match new_user_type.lower():  # Make sure the type entered is valid.
                                case "standard user" | "standard" | "user" | "basic":
                                    new_user_type = "StandardUser"
                                    break
                                case "administrator" | "admin" | "advanced":
                                    new_user_type = "Administrator"
                                    break
                                case "help":
                                    print("\n1. Standard Users have limited privileges, such as editing their own user settings, personalization, and running applications.")
                                    print("2. Administrators have all privileges, and can edit other users' settings, and install/uninstall applications.")
                                case "":
                                    break
                                case _:
                                    Loading.returning("That is not a valid user type.", 2)
                        if new_user_type in ("StandardUser", "Administrator"):
                            new_option = input("What should the new user be named? Alphanumeric, case-sensitive, no escape characters.")  # Ask for user details.
                            new_user_pwd = input("What is the password for this new user?")
                            if not new_user_pwd:  # Carry-over from user_settings.py to set the default password.
                                Loading.returning('The default password is "python123".')
                                new_user_pwd = "python123"
                            elif input("Password set. Type it again to confirm.") != new_user_pwd:  # Confirming the password!
                                Loading.returning("The passwords you entered don't match.", 2)
                                continue
                            if not all(i in Loading.ALPHABET for i in new_option):  # Making sure escape characters aren't present.
                                Loading.returning("Make sure your username is alphanumeric. Escape characters are not supported.", 2)
                            elif new_option == "Default" or new_option in [i.username for i in self.os_object.users]:  # Avoiding users with the same name.
                                Loading.returning("That username is taken.", 2)
                            else:  # If everything checks out, add the new user!
                                new_user = None
                                try:  # Handling the errors in case they occur. Anything can happen!
                                    new_user = User.__getattribute__(new_user_type)(username=new_option, password=new_user_pwd, current=False)
                                    self.os_object.users.append(new_user)
                                    os.makedirs(self.os_object.path.format(new_option))
                                    file = open('Users\\{}\\info.usr'.format(new_option), 'w')
                                    file.write(Loading.caesar_encrypt(new_user.__repr__()))
                                    file.close()
                                except (KeyError, IndexError, NotImplementedError, OSError, FileNotFoundError, FileExistsError):
                                    Loading.returning("An error has occurred while creating the new user. Please try again.")
                                    try:  # Attempt to undo whatever happened.
                                        self.os_object.users.remove(new_user)
                                        os.rmdir(self.os_object.path.format(new_option))
                                        os.remove("Users\\{}\\info.usr".format(new_option))
                                        os.rmdir(self.os_object.path.format(new_option))
                                    except (KeyError, IndexError, NotImplementedError, OSError, FileNotFoundError, FileExistsError):
                                        pass  # If any of the undoing fails, that means it was never done, and we can safely exit.
                                    finally:
                                        continue
                                Loading.returning("User has been created!")  # Perfect!
                    else:
                        Loading.returning("You do not have the required privileges to create a new user.", 3)
                        continue
                case "edit username" | "username" | "name" | "uname" | "edit username" | "edit name" | "edit uname" |\
                     "edit password" | "password" | "pwd" | "edit pwd":  # Handling both changing usernames and passwords here.
                    changing_password = True if choice.lower() in ("edit password", "password", "pwd", "edit pwd") else False
                    user_select = print_all_users(message="What {option!s} would you like to edit?".format(  # Check if the current user is admin.
                        option="password" if changing_password else "username"), access=2) if self.os_object.current_user.elevated else self.os_object.current_user
                    if user_select:
                        new_option = input("What is the new {option!s}?".format(option="password" if changing_password else "username"))
                        if not all(i in Loading.ALPHABET for i in new_option):
                            Loading.returning("Make sure your username is alphanumeric. Escape characters are not supported.", 2)
                        elif (not changing_password) and (new_option == "Default" or new_option in [i.username for i in self.os_object.users]):  # Avoiding users with the same name.
                            Loading.returning("That username is taken.", 2)
                        elif changing_password:
                            if new_option != input("Type in the new password again to confirm it."):
                                Loading.returning("The passwords do not match. Try again", 2)
                        else:  # If everything checks out, change the option!
                            if changing_password:
                                user_select.password = new_option
                            else:
                                user_select.username = new_option
                            Loading.returning("{option!s} has been changed!".format(option="Password" if changing_password else "Username"), 2)
                case "delete user" | "delete" | "del":
                    if self.os_object.current_user.elevated:
                        user_select = print_all_users(message="Which user would you like to delete?", access=1)
                        try:
                            self.os_object.recently_deleted_users.append(user_select)
                            self.os_object.users.remove(user_select)
                        except ValueError:
                            Loading.returning("An error has occurred. Please safely reboot the system.", 2)
                    else:
                        Loading.returning("You do not have the required privileges to delete users.", 3)
                        return
                case "restore user" | "restore" | "resurrect" | "res":
                    if self.os_object.current_user.elevated:
                        if self.os_object.recently_deleted_users:
                            print("\n".join(["{number!s}. {name!s}".format(number=i+1, name=self.os_object.recently_deleted_users[i].username) for i in range(len(self.os_object.recently_deleted_users))]))
                            user_select = input("Which user would you like to restore")
                            try:
                                user_select = [i for i in self.os_object.recently_deleted_users if i.username == user_select][0]
                                self.os_object.users.append(user_select)
                                self.os_object.recently_deleted_users.remove(user_select)
                            except IndexError:
                                Loading.returning("That is not a valid username.")
                            except ValueError:
                                Loading.returning("An error has occurred. Please safely reboot the system.", 2)
                        else:
                            Loading.returning("There are no recently deleted users.", 2)
                    else:
                        Loading.returning("You do not have the required privileges to restore users.", 3)
                        return
                case "" | "exit" | "get me outta here":
                    break
                case _:
                    Loading.returning("Please choose from the list of options." | 2)
        return

    def updates(self):
        """
        Method for the Update Settings Sub-menu.
        :return: Nothing.
        """
        while True:
            Settings.settings_menu("SETTINGS", self.entries, "Updates", self.os_object.current_user.color)
            choice = input()
            match choice.lower():
                case "check for updates" | "check updates" | "check":
                    os_file = requests.get("https://raw.githubusercontent.com/Cerberus1470/Serpens-Vivus/Tejas/System/operating_system.py")
                    # module_names = sorted([i.__name__ for i in operating_system.apps.values() for i in i])  For later :)
                    if os_file.status_code == 200:
                        version_remote = float([i for i in os_file.text.split('\n') if 'version = ' in i][0].split('"')[1]
                                               .replace("_", "").replace('alpha', '1').replace('beta', '2').replace('gamma', '3'))
                        version_local = float(operating_system.version.replace("_", "").replace('alpha', '1').replace('beta', '2').replace('gamma', '3'))
                        if version_remote > version_local:
                            if input("There is a new update available: POCS {version}!\nWould you like to download it?".format(version=version_remote)) in ('yes', 'y', 'of course', 'absolutely'):
                                try:
                                    open("System\\operating_system.py", 'w').write(os_file.text)
                                except (io.UnsupportedOperation, OSError):
                                    Loading.returning("The update failed to install. Please re-download the OS from GitHub and reboot.")
                        elif version_remote == version_local:
                            Loading.returning("You are on the latest version of POCS: {version}".format(version=version_local), 2)
                        else:
                            Loading.returning("Somehow, you are ahead of the public release. Are you a developer by chance?", 2)

                    else:
                        Loading.returning("The System was unable to find the latest release.")
                case "" | "exit" | "leave!!!":
                    break
                case _:
                    Loading.returning("Please choose from the list of options.", 2)
        return

    def recovery(self):
        """
        Method for the System Recovery Setting Sub-menu.
        :return: Nothing/
        """
        from System import recovery
        import shutil
        while True:
            Settings.settings_menu("SETTINGS", self.entries, "Recovery", self.os_object.current_user.color)
            choice = input()
            match choice.lower():
                case "verify os integrity" | "verify" | "os" | "integrity" | "verify os" | "verify integrity" | "os integrity":
                    try:
                        self.os_object.reload()
                        # This is pretty much it. If any of the python files were corrupted or broken, the runtime would've called it out during import.
                        Loading.progress_bar("Verifying OS Integrity...", 10)  # Visuals!
                        Loading.returning("\nOS integrity verified. Your system has no faults.", 2)
                    except (Exception, recovery.CorruptedFileSystem, recovery.NoAdministrator, recovery.NoCurrentUser, recovery.CorruptedRegistry) as error:  # All raised by reload()
                        Loading.returning("The OS detected faults in the User files. Please launch System Recovery.", 3)
                case "back up files" | "backup" | "restore" | "file backup":
                    # TODO: Features: Custom path, Custom uptime-based frequency, custom elements to back up, where to put each thing? Also make it a single file.
                    if not os.path.exists("System\\BACKUP"):
                        if input("This system can back up your files to keep them safe.\nWould you like to set up Backup now?").lower() in ('yes', 'y', 'of course', 'absolutely', 'setup backup', 'setup', 'backup'):
                            try:
                                shutil.copytree("System\\REGISTRY", "System\\BACKUP\\REGISTRY")
                                shutil.copytree("Users", "System\\BACKUP\\Users")
                                Loading.progress_bar("Backing up files...", 2 * len(self.os_object.users))  # Visuals
                                Loading.returning("\nThe OS has finished backing up your files.", 2)
                            except (shutil.Error, FileExistsError):  # Undo the backup creation
                                shutil.rmtree("System\\BACKUP", ignore_errors=True)
                                Loading.returning("The OS failed to back up the system. Try again later.", 3)
                    else:
                        match input("There is already a backup stored. Would you like to restore from it, update it, or delete it?").lower():
                            case "restore from it" | "restore it" | "restore" | "restore from backup" | "restore backup":
                                backup_os_object = None
                                try:
                                    backup_os_object = self.os_object.copy()
                                    shutil.copytree("System\\BACKUP\\REGISTRY", "System\\REGISTRY", dirs_exist_ok=True)
                                    shutil.copytree("System\\BACKUP\\Users", "Users", dirs_exist_ok=True)
                                    self.os_object.reload()
                                    Loading.progress_bar("Restoring from Backup...", 2 * len(self.os_object.users))  # Visuals
                                    Loading.returning("\nThe OS has finished restoring your backup. Please reboot the system.", 2)
                                except (shutil.Error, FileExistsError, recovery.CorruptedFileSystem, recovery.NoAdministrator, recovery.NoCurrentUser, recovery.CorruptedRegistry) as error:  # Undo everything!
                                    backup_os_object.registry.verify_build(["Resolution", "Recovery", "Speed"] + ["SVKEY_USER\\{user}\\Start".format(user=i.username.upper()) for i in self.users])  # Restore the Registry.
                                    for i in backup_os_object.users:  # Now write each user's info to their respective info files.
                                        os.makedirs(backup_os_object.path.format(i.username), exist_ok=True)
                                        open(backup_os_object.path.format(i.username) + "\\info.usr", 'w').write(Loading.caesar_encrypt(i.__repr__()))
                                    Loading.returning("The OS failed to restore the backup and has attempted to restore your most recent backup.", 3)
                            case "update it" | "update" | "update backup":
                                try:
                                    shutil.copytree("System\\REGISTRY", "System\\BACKUP\\REGISTRY", dirs_exist_ok=True)
                                    shutil.copytree("Users", "System\\BACKUP\\Users", dirs_exist_ok=True)
                                    Loading.progress_bar("Backing up files...", 2 * len(self.os_object.users))  # Visuals
                                    Loading.returning("\nThe system has finished backing up your files.", 2)
                                except (shutil.Error, FileExistsError):  # Undo the backup creation
                                    shutil.rmtree("System\\BACKUP", ignore_errors=True)
                                    Loading.returning("The OS failed to back up the system. Try again later.", 2)
                            case "delete it" | "delete" | "delete backup":
                                try:
                                    shutil.rmtree("System\\BACKUP")
                                    Loading.progress_bar("Deleting Backup...", 5)  # Visuals
                                    Loading.returning("\nThe OS has finished restoring your backup. Please reboot the system.", 2)
                                except (shutil.Error, NotImplementedError):
                                    Loading.returning("The OS failed to delete the backup. Try again later.", 2)
                case "reset" | "reset system" | "reset settings":
                    match input("\n{ln}RESET{ln}\n1. All Users\n2. Registry\n3. All Settings\n\nWhat would you like to reset?".format(ln="-" * 10)).lower():
                        case "all users" | "users" | "user" | "user info":
                            reset = "user data"
                        case  "registry" | "reg" | "the registry" | "the reg":
                            reset = "registry keys"
                        case "all settings" | "all" | "everything" | "the whole lot" | "burn it":
                            reset = "settings"
                        case "":
                            continue
                        case _:
                            Loading.returning("Please choose a valid option.")
                            continue
                    Loading.returning("Please note that these actions are IRREVERSIBLE.", 2)
                    if input("Are you sure you want to reset all {reset}? This action cannot be undone.".format(reset=reset)) in ('yes', 'y', 'of course', 'absolutely'):
                        try:
                            shutil.rmtree([i for i in (["Users\\"] if reset == "user data" else ["System\\REGISTRY\\"] if reset == "registry keys" else ["Users\\", "System\\REGISTRY\\"])])
                            Loading.progress_bar("Resetting {reset}...".format(reset=reset), 2 * len(self.os_object.users))
                            Loading.returning("{reset} successfully reset. The system will now shutdown.".format(reset=reset.capitalize()), 2)
                            exit()
                        except(shutil.Error, NotImplementedError, TypeError):
                            Loading.returning("The OS failed to reset your {reset}. Please shutdown the system.".format(reset=reset), 2)
                case "" | "exit" | "burger with no honey mustard":
                    break
                case _:
                    Loading.returning("Please choose from the list of options.", 2)
