"""
Program full of nothing at the moment.
"""

from System import Loading


class Settings:
    """
    Main class to house everything!
    """
    category = "utilities"

    def __init__(self, os_object, color):
        self.user_color = color
        self.os_object = os_object
        self.entries = {"Personalize": ("Edit Text Color", "Edit Background", "Change Animation Speed"),
                        "Users": ("Add New User", "Edit Username", "Edit Password", "Delete User", "Restore User", "Switch User"),
                        "Updates": ("Check for Updates", "Install Updates", "Update History"),
                        "Recovery": ("Verify OS Integrity", "Back Up Files", "Reset")}
        return

    def __repr__(self):
        return

    @staticmethod
    def boot(os_object):
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
            # for i in list(self.entries.keys()):
            #     print("\n\033[4m{}\033[0;{}m".format(i, self.user_color))
            choice = Loading.pocs_input()
            match choice.lower():
                case "personalize":
                    self.personalize()
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
                    new_color = input("What would you like your text color to be? Current Color: {!s}".format(self.user_color))
                    if new_color in Loading.COLORS:
                        self.os_object.current_user.color = self.user_color = Loading.COLORS[new_color]
                    elif new_color in list(Loading.COLORS.values()):
                        self.os_object.current_user.color = self.user_color = new_color
                    else:
                        Loading.returning("That is not a valid color. Here is a list of valid colors:\n{}".format("\n".join([i for i in list(Loading.COLORS.keys())])), 5)
                    print("\033[0;{}m".format(self.user_color))
                case "edit background" | "edit" | "background":
                    for i, v in enumerate(Loading.BACKGROUNDS):
                        print("{}. {}".format(i + 1, v))
                    new_bg = input("Which background would you like? Current Background: {!s}".format(self.os_object.current_user.background))
                    if new_bg in [i.split('.')[0] for i in Loading.BACKGROUNDS] or new_bg in Loading.BACKGROUNDS:
                        self.os_object.current_user.background = new_bg + ".bg" if ".bg" not in new_bg else ""
                    else:
                        Loading.returning("That is not a valid background.", 2)
                case "change animation speed" | "animation" | "speed" | "change animation" | "change speed" | "animation speed":
                    try:
                        new_anim_speed = float(input("What should the new animation speed be (i.e. 1 = 1x, 2 = 2x, 0.5 = 0.5x)? Current Factor: {!s}".format(self.os_object.current_user.speed)))
                        if new_anim_speed <= 0:
                            raise ValueError
                    except ValueError:
                        Loading.returning("That is not a valid speed factor.", 2)
                    else:
                        self.os_object.current_user.speed = new_anim_speed
                        Loading.SPEED = new_anim_speed
                    pass  # TODO Add changing animation speed here!
                case "reset_personalize":
                    self.os_object.current_user.color = 0
                    self.os_object.current_user.background = "pyidea.bg"
                    self.os_object.current_user.speed = 1.0
                    return
                case "" | "exit" | "please":
                    return
                case _:
                    Loading.returning("Please choose from the list of options.", 2)

    #         choice = input("""
    # SETTINGS\t\t\t|
    # \033[4mPersonalize\033[0;{}m - - - - |\tEdit Text Color
    # Users\t\t\t\t|\tEdit Background
    # Updates\t\t\t\t|\tEdit Animation Speed
    # Recovery\t\t\t
    # \t\t\t\t\t""".format(self.user_color)).lower()

    def users(self):
        """
        Method for the Users Settings Sub-menu.
        :return: Nothing.
        """
        Settings.settings_menu("SETTINGS", self.entries, "Users", self.user_color)
        while True:
            choice = input()
            match choice.lower():
                case "add new user" | "add" | "new" | "add new" | "add user" | "new user":
                    pass  # TODO: Add the new add user Wizard!
                case "edit username" | "username" | "name" | "uname" | "edit name" | "edit uname":
                    pass  # TODO: Add edit username wizard here!
                case "edit password" | "password" | "pwd" | "edit pwd":
                    pass  # TODO: Add edit password wizard here!
                case "delete user" | "delete" | "del":
                    pass  # TODO: Add new delete user Wizard!
                case "restore user" | "restore" | "resurrect" | "res":
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
        Settings.settings_menu("SETTINGS", self.entries, "Updates", self.user_color)
        while True:
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
        Settings.settings_menu("SETTINGS", self.entries, "Recovery", self.user_color)
        while True:
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
