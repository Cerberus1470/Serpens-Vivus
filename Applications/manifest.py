"""
Application for administrators to modify the registry. Will include security that asks for elevation or denies access.
"""

import os
from System import Loading, Registry, recovery

category = "admin"
version = "1.0"
entries = ("manifest", "registry")


def boot(os_object=None):
    """
    This method regulates the startup process for this application.
    :param os_object: The OS Object, used to obtain the current Registry.
    :return: Nothing
    """
    manifest = Manifest(os_object)
    manifest.main()


class Manifest:
    """
    Main class that houses the Manifest application.
    """

    def __init__(self, os_object: None = None):
        self.os_object = os_object
        return

    def __repr__(self):
        return

    @staticmethod
    def registry_menu(title: str = "TITLE", dictionary: dict = None, selected_key: str = "", color: int = 0):
        """
        A universal method to print out a "graphical" menu with provided materials.
        :param title: The title to display at the top of the menu.
        :param dictionary: The dictionary provided.
        :param selected_key: The selected category from which to display options.
        :param color: The color for formatting the text to.
        :return: Nothing. This method is meant to print everything by itself.
        """
        if not dictionary:
            print("{}\nThis folder is empty.".format(title))
            return
        max_len = len(max(dictionary.keys(), key=len))
        margin = (int(max_len / 8) + (2 if max_len % 8 else 1)) * 8
        print("\nComputer{slash}{folder}".format(slash="\\" if title else "", folder=title))
        if selected_key:  # If a key is selected
            options = ("Edit Key", "Rename Key", "Delete Key",)
        else:
            options = ("Add Key",)
        for index, key in enumerate(list(dictionary.keys())):
            print("|---" if index != len(dictionary.keys()) - 1 else "'---", end="")  # Print prefix
            print("\033[4m{category}\033[0;{}m".format(color, category=key) if key == selected_key else key, end="")  # Print folder/file name
            print("{}|".format(" " * (margin - len(key))), end="")
            try:
                print("        {}. {}".format(index+1, options[index]), end="")
            except IndexError:
                pass
            print()
            continue
        if len(dictionary.keys()) <= 3:  # What if there aren't enough entries to write all the options?
            for over_index in range(len(dictionary.keys()), 3 if selected_key else 1):
                print("    {}|        {}. {}".format(" " * margin, over_index+1, options[over_index]))
        return

    def main(self):
        """
        Main wrapper method that keeps the user in the application.
        Adapted from the main method of Cabinet, with added code for registry keys.
        :return:
        """
        print("Welcome to the Manifest.")
        folder = ""
        file = None
        while True:  # Main input loop.
            tree = list(os.scandir("System\\REGISTRY\\" + folder))
            self.registry_menu("" if folder == "." else folder, dict.fromkeys([i.name for i in tree]), selected_key=file.name if file else "")
            choice = input("\nSelect a folder or key to open.").lower()
            if choice in ("help", "help me", "pls halp", "i need assistance", "what do i do"):  # Offer some assistance.
                input("""Welcome to the Manifest. This is a comprehensive application that allows you to edit the System Registry.
The registry is a complex set of keys and directories that stores vital information for the OS. 
Things like your start menu categorization and the speed of system animations. Certain games may also store values in the Registry for later use.
As an administrator, you can also directly edit registry keys using this app. Be wary, though, as these changes may harm the functionality of the OS or other applications.""")
                input("""You will be greeted with an interface similar to the Cabinet app, where you can navigate through the system registry.
Type the name of a folder to navigate into it, the name of a key to see options, or type "add key" to add a new key. Type nothing to go back up a folder.
After making your changes, you can also type "reload" to verify and recreate the registry in memory to ensure it does not break the OS.

If you need to see this message again, just type "help".""")
                continue
            if file:  # A key is selected, check for options.
                path = file.path.replace(self.os_object.registry.base_path, "").replace(".svkey", "")
                match choice:
                    case "edit" | "edit key" | "1" | "one" | "change" | "change key" | "modify" | "modify key":  # Edit the key.
                        print("Current Value for key {}: {}".format(file.name, self.os_object.registry.get_svkey(path)))
                        self.os_object.registry.set_svkey(path, input("New value for registry key {name}?".format(name=file.name)))
                    case "rename" | "rename key" | "2" | "two" | "new name":  # Rename the key filename.
                        self.os_object.registry.add_svkey(os.path.join(folder, input("New name for key {}: ".format(file.name))), self.os_object.registry.get_svkey(path))
                        self.os_object.registry.delete_svkey(path)
                    case "delete" | "delete key" | "remove" | "remove key" | "3" | "three" | "destroy it" | "burn this":  # Delete the key!
                        self.os_object.registry.delete_svkey(path)
                file = None
                continue
            if choice in ("", "back", "up", "previous", "level", "travel"):  # Nothing, move up a folder.
                if not folder:
                    Loading.returning_to_apps()
                    return
                folder = folder.rpartition("\\")[0]
                continue
            if choice in ("reload", "refresh", "reload registry", "refresh registry"):  # Reload the registry
                self.os_object.registry = Registry.Registry("System\\REGISTRY", self.os_object.elevate)
                if self.os_object.registry.verify_build(["Resolution", "Recovery", "Speed"] + ["SVKEY_USER\\{user}\\Start".format(user=i.username.upper()) for i in self.os_object.users]):
                    Loading.SPEED = float(self.os_object.registry.get_key("Speed"))
                    Loading.returning("Registry contents reloaded successfully.", 2)
                else:  # If required keys are not present...
                    raise recovery.CorruptedRegistry(self.os_object.registry)
                continue
            if choice in ("1", "one", "add", "add key", "create", "create key", "new", "new key", "create new", "create new key", "add new", "add new key"):  # Add a new key?
                key = input("Name for the new Registry Key?")
                key += '\n' if '\\' in key else ""  # Adding an intentional escape character to block against directory creation.
                self.os_object.registry.add_svkey(os.path.join(folder, key), input("Value for {}: ".format(key)))
                continue
            for i in tree:  # Otherwise, check if the user entered a directory/key name.
                if (choice == i.name.lower()) and i.is_dir():  # Is the choice a valid directory?
                    if folder == ".":
                        folder = i.name
                        break
                    folder = os.path.join(folder, i.name)
                    break
                elif (choice == i.name.lower() or choice + ".svkey" == i.name.lower()) and i.is_file():  # A key?
                    file = i
                    break
            else:  # For loop exhausted
                Loading.returning("Please choose a valid option.", 2)
