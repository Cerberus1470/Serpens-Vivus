"""
Program full of nothing at the moment.
"""

from System.User import *


class Settings:
    """
    Main class to house everything!
    """
    category = "utilities"

    def __init__(self, os_object : None = None, color : int = 0):
        self.user_color = color
        self.os_object = os_object
        self.entries = {"Personalize": ("Edit Text Color", "Edit Background", "Change Animation Speed"),
                        "System": ("Resolution", ),
                        "Users": ("Add New User", "Edit Username", "Edit Password", "Delete User", "Restore User", "Switch User"),
                        "Updates": ("Check for Updates", "Install Updates", "Update History"),
                        "Recovery": ("Verify OS Integrity", "Back Up Files", "Reset")}
        return

    def __repr__(self):
        return

    # noinspection PyUnresolvedReferences
    # The object passed by the OS will always be the os_object. If it's not, someone else is calling the method.
    @staticmethod
    def boot(os_object : None = None):
        """
        This method regulates the startup process for this application.
        :param os_object: The OS Object, used to obtain the current user's text color.
        :return: Nothing
        """
        settings = Settings(os_object, os_object.current_user.color)
        settings.main()

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
            return "The dictionary is empty."
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
            Settings.settings_menu("SETTINGS", self.entries, color=self.user_color)
            # Trying an iterative logic net as opposed to hardcoded match-case. Not enough entries to warrant though.
            # try:
            #     choice = [i for i in self.entries.keys() if Loading.pocs_input().equals(i)][0]
            #
            # except IndexError:
            #     Loading.returning("Please choose from the list of choices.", 2)
            choice = Loading.pocs_input()
            match choice.lower():
                case "personalize":
                    self.personalize()
                case "system":
                    self.system()
                case "users":
                    self.users()
                case "updates":
                    self.updates()
                case "recovery":
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
            Settings.settings_menu("SETTINGS", self.entries, "Personalize", self.user_color)
            choice = input()
            match choice.lower():
                case "edit text color" | "color" | "text" | "edit color" | "edit text" | "text color":
                    new_color = input("What would you like your text color to be? Current Color: {!s}\n".format(self.user_color))
                    if new_color in Loading.COLORS:
                        self.os_object.current_user.color = self.user_color = Loading.COLORS[new_color]
                    elif new_color in list(Loading.COLORS.values()):
                        self.os_object.current_user.color = self.user_color = new_color
                    else:
                        Loading.returning("That is not a valid color.", 5)
                        print("Here is a list of valid colors:\n{}".format("\n".join([i for i in list(Loading.COLORS.keys())])))
                    print("\033[0;{}m".format(self.user_color))
                case "edit background" | "edit" | "background":
                    for i, v in enumerate(Loading.BACKGROUNDS):
                        print("{}. {}".format(i + 1, v))
                    new_bg = input("Which background would you like? Current Background: {!s}\n".format(self.os_object.current_user.background))
                    if new_bg in [i.split('.')[0] for i in Loading.BACKGROUNDS] or new_bg in Loading.BACKGROUNDS:
                        self.os_object.current_user.background = new_bg + (".bg" if ".bg" not in new_bg else "")
                    else:
                        Loading.returning("That is not a valid background.", 2)
                case "change animation speed" | "animation" | "speed" | "change animation" | "change speed" | "animation speed":
                    try:
                        new_anim_speed = float(input("What should the new animation speed be (i.e. 1 = 1x, 2 = 2x, 0.5 = 0.5x)? Current Factor: {!s}\n".format(self.os_object.current_user.speed)))
                        if new_anim_speed <= 0:
                            raise ValueError
                    except ValueError:
                        Loading.returning("That is not a valid speed factor.", 2)
                    else:
                        self.os_object.current_user.speed = new_anim_speed
                        Loading.SPEED = new_anim_speed
                    pass
                case "reset_personalize":
                    self.os_object.current_user.color = self.user_color = 0
                    self.os_object.current_user.background = "pyidea.bg"
                    self.os_object.current_user.speed = Loading.SPEED = 1.0
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
            Settings.settings_menu("SETTINGS", self.entries, "System", self.user_color)
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
                    Loading.Registry.modify_registry("Resolution", "SVKEY_SYSTEM", new_resolution)

    def users(self):
        """
        Method for the Users Settings Sub-menu. Built from the ground up based on the deprecated user_settings.py app.
        :return: Nothing.
        """
        def print_all_users(message : str = "Select a User.", access : int = 0) -> User:
            """
            Method to print a numbered list of all users currently registered. Allows selection of a valid user based on priority.
            Returns PermissionError if access level is not 0, 1, or 2.
            :param message: Message to display when collecting input.
            :param access: Level of input privilege elevation. 0 means do not collect, 1 mean Standard Users, 2 means Admins and Standard.
            :return: The selected user.
            """
            print("\n".join(["{number!s}. {name!s}".format(number=i, name=self.os_object.users[i].username) for i in range(len(self.os_object.users))]))
            if access == 0:  # If priority is 0 (default), do not collect input.
                return
            elif access == 1 or access == 2:
                user_select_master = input(message)
                try:
                    user_select_master = [i for i in self.os_object.users if i.username == user_select_master][0]
                    if access == 1 and user_select_master.__class__ == Administrator and user_select_master != self.os_object.current_user:
                        Loading.returning("You do not have enough privileges to alter other administrators.", 2)
                    else:
                        return user_select_master
                except IndexError:
                    Loading.returning("That is not a valid username.", 2)
                    return
            else:  # If the access level is not 0, 1, or 2.
                raise PermissionError("That access level is not valid.")
        while True:  # The main while loop for users.
            Settings.settings_menu("SETTINGS", self.entries, "Users", self.user_color)
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
                            if "\\" in new_option or '\\' in new_user_pwd:  # Making sure escape characters aren't present.
                                Loading.returning("Escape characters are not supported.", 2)
                            elif new_option == "Default" or new_option in [i.username for i in self.os_object.users]:  # Avoiding users with the same name.
                                Loading.returning("That username is taken.", 2)
                            else:  # If everything checks out, add the new user!
                                new_user = None
                                try:  # Handling the errors in case they occur. Anything can happen!
                                    new_user = globals()[new_user_type](username=new_option, password=new_user_pwd, current=False)
                                    self.os_object.users.append(new_user)
                                    os.mkdir('Users\\{}'.format(new_option))
                                    file = open('Users\\{}\\info.usr'.format(new_option), 'w')
                                    file.write(Loading.caesar_encrypt(new_user.__repr__()))
                                    file.close()
                                except (KeyError, IndexError, NotImplementedError, OSError, FileNotFoundError):
                                    Loading.returning("An error has occurred while creating the new user. Please try again.")
                                    try:  # Attempt to undo whatever happened.
                                        self.os_object.users.remove(new_user)
                                        os.rmdir("Users\\{}".format(new_option))
                                        os.remove("Users\\{}\\info.usr".format(new_option))
                                    except (KeyError, IndexError, NotImplementedError, OSError, FileNotFoundError):
                                        pass  # If any of the undoing fails, that means it was never done, and we can safely exit.
                                Loading.returning("User has been created!")  # Perfect!
                    else:
                        Loading.returning("You do not have the required privileges to create a new user.", 3)
                        return
                case "edit username" | "username" | "name" | "uname" | "edit name" | "edit uname" | "edit password" | "password" | "pwd" | "edit pwd":  # Handling both changing usernames and passwords here.
                    changing_password = False
                    if choice.lower() in ("edit password", "password", "pwd", "edit pwd"):
                        changing_password = True
                    if self.os_object.current_user.elevated:  # Check if the current user is admin.
                        user_select = print_all_users(message="What {option!s} would you like to edit?".format(
                            option="password" if changing_password else "username"), access=1)
                    else:
                        user_select = self.os_object.current_user
                    new_option = input("What is the new {option!s}?".format(option="password" if changing_password else "username"))
                    if "\\" in new_option:  # Making sure escape characters aren't present.
                        Loading.returning("Escape characters are not supported.", 2)
                    elif (not changing_password) and (new_option == "Default" or new_option in [i.username for i in self.os_object.users]):  # Avoiding users with the same name.
                        Loading.returning("That username is taken.", 2)
                    elif changing_password:
                        if new_option != input("Type in the new password again to confirm it."):
                            Loading.returning("The passwords do not match. Try again", 2)
                    else:  # If everything checks out, change the name!
                        if changing_password:
                            user_select.password = new_option
                        else:
                            user_select.username = new_option
                        Loading.returning("{option!s} has been changed!".format(option="Password" if changing_password else "Username"))
                    pass  # TODO: Add edit username wizard here!
                case "edit password" | "password" | "pwd" | "edit pwd":
                    pass  # TODO: Add edit password wizard here!
                    # Implemented above.
                case "delete user" | "delete" | "del":
                    if self.os_object.current_user.elevated:
                        user_select = print_all_users(message="Which user would you like to delete?", access=1)
                        try:
                            self.os_object.users.remove(user_select)
                            self.os_object.recently_deleted_users.append(user_select)
                        except ValueError:
                            Loading.returning("An error has occurred. Please safely reboot the system.", 2)
                    else:
                        Loading.returning("You do not have the required privileges to delete users.", 3)
                        return
                    pass  # TODO: Add new delete user Wizard!
                case "restore user" | "restore" | "resurrect" | "res":
                    if self.os_object.current_user.elevated:
                        if self.os_object.recently_deleted_users:
                            print("\n".join(["{number!s}. {name!s}".format(number=i, name=self.os_object.recently_deleted_users[i].username) for i in range(len(self.os_object.recently_deleted_users))]))
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
                        Loading.returning("You do not have the required privileges to restore users.", 3)
                        return
                    pass  # TODO: Add restore user Wizard!
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
            Settings.settings_menu("SETTINGS", self.entries, "Updates", self.user_color)
            choice = input()
            match choice.lower():
                case "check for updates" | "check updates" | "check":
                    pass  # TODO: Add check for updates wizard here!
                case "install updates" | "install" | "update":
                    pass  # TODO: Add install updates wizard here!
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
        while True:
            Settings.settings_menu("SETTINGS", self.entries, "Recovery", self.user_color)
            choice = input()
            match choice.lower():
                case "verify os integrity" | "verify" | "integrity" | "verify os" | "verify integrity" | "os integrity":
                    pass  # TODO: Add OS integrity check wizard here!
                case "back up files" | "backup" | "restore" | "file backup":
                    pass  # TODO: Add backup/restore wizard here!
                case "reset" | "reset system" | "reset settings":
                    pass  # TODO: Add reset system wizard here!
                case "" | "exit" | "burger with no honey mustard":
                    break
                case _:
                    Loading.returning("Please choose from the list of options.", 2)
