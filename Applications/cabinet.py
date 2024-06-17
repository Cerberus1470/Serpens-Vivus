"""
Module Cabinet. System application that handles file management.
"""
import os
from System import Loading

category = "utilities"
version = "1.0"
entries = ("cabinet", "files", "explorer", "file manager", "file explorer")


def boot(_):
    """
    Used to regulate the boot-up process.
    :return: Nothing
    """
    Cabinet.main()


class Cabinet:
    """
    Class Cabinet. Houses the main application for the file manager.
    """
    def __init__(self):
        pass

    def __repr__(self):
        pass

    @staticmethod
    def main():
        """
        The main method for the file manager.
        :return: Nothing
        """
        """
        Pseudocode: internal recursive method displaying file and directory structure. Shown in a tree format, graphically. Users type directory names to navigate,
        and can type filenames to open them. Opening files from file manager should append either a HomeInterrupt or LockInterrupt object with default values for 
        the game. That way, when the user returns to the home screen, they launch into the app or the game. Should work nicely, but each app with file management
        should handle Interrupt objects properly!
        Should look like:
        root
        |---Applications
        |---Bug Trackers
        |---System
        |   |---BACKUP
        |   |---bg
        |   |   |---10x40
        |   |   |---20x80
        |   |   |---30x120
        |   |   |   |---airplane.bg
        |   |   |   |---pyidea.bg
        |   |   |   |---mountains.bg
        |   |   |   '---waterfall.bg
        |   |   '---40x160
        |   |---REGISTRY
        |   |---event_log.info
        |   |---Loading.py
        |   |---operating_system.py
        |   |---recovery.py
        |   |---Registry.py
        |   '---User.py
        '---Users
        """
        folder = "."
        while True:
            tree = [i for i in os.scandir(folder) if any([j in ("Applications", "Bug Trackers", "System", "Users") for j in i.path.split("\\")])]
            print("{dir}\n{folders}".format(dir=folder, folders='\n'.join(("|---" if i != len(tree)-1 else "'---") + tree[i].name for i in range(len(tree)))))
            choice = input("\nSelect a folder or file to open.")
            if choice in [i.name for i in tree]:  # Make sure the choice is valid.
                if [i for i in tree if i.name == choice][0].is_dir():  # Check if it's a directory.
                    folder += "\\" + choice
                else:
                    pass  # TODO: Add opening files here!
            elif choice in ("", "back", "up"):
                folder = folder.rpartition("\\")[0]
                if not folder:
                    return
            else:
                Loading.returning("Please choose a valid option.", 2)

