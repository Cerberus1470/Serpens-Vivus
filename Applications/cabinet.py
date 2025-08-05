"""
Module Cabinet. System application that handles file management.
"""
import os
from System import Loading

category = "utilities"
version = "1.2_alpha01"
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
            print("{dir}\n{folders}".format(dir=folder, folders='\n'.join(("|---" if i != len(tree) - 1 else "'---") + tree[i].name for i in range(len(tree)))))
            choice = input("\nSelect a folder or file to open.")
            if choice in [i.name for i in tree]:  # Make sure the choice is valid.
                if [i for i in tree if i.name == choice][0].is_dir():  # Check if it's a directory.
                    folder += "\\" + choice
                else:  # Should be a file at this point.
                    pass  # TODO: Add opening files here! Use open_file() and then use that to create a HomeInterrupt, then return to home to open the file.
                    # I don't want to deal with scope, calling main() methods from the Cabinet, so I'm going to quit cabinet and launch the game using
                    # already set-up OS features.
            elif choice in ("", "back", "up"):
                folder = folder.rpartition("\\")[0]
                if not folder:
                    return
            else:
                Loading.returning("Please choose a valid option.", 2)


class FileEngine:
    """
    Class FileEngine. Houses widely-used methods to read from, delete, and write to files.
    """

    @staticmethod
    def init(self, path : str = "\\", extension : str = ""):
        """
        Method to select a game file.
        :param self: Game object.
        :param path: Path to search in.
        :param extension: File extension to filter to. Will be just the extension.
        :return: Either raw game data or translated game data
        """
        while True:
            count = 0
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    if file.rpartition(".")[2] == extension:
                        count += 1
                        print('{count}. {file}'.format(count=count, file=file))
            print('{}. New File\n{}. Delete File'.format(str(count + 1), str(count + 2)))
            self.filename = input('Which file would you like to open? Type "exit" to exit.\n').replace(".{ext}".format(ext=extension), "")
            if self.filename.lower() in ("", "exit", "leave", "get me outta here"):
                Loading.returning_to_apps()
                return
            if self.filename.lower() in ("new file", "new", "brand new", "new game", "new note"):
                self.new_file = True
                return ""
            elif self.filename.lower() in ("delete file", "delete", "delete game", "delete note"):
                FileEngine.delete(path, extension)
            else:
                try:
                    game = list(open("{}\\{}".format(path, '{}.{}'.format(self.filename, extension)), 'r'))
                    self.filename = '{}.{}'.format(self.filename, extension)
                    Loading.progress_bar("Loading save file...", 1)
                    return (Loading.caesar_decrypt(game[0].replace('\n', ''))).split('(G)')
                except FileNotFoundError:
                    Loading.returning("Choose a valid option.", 1)

    @staticmethod
    def delete(path, extension : str = ""):
        """
        Method to delete a game file.
        :param path: Path to search in.
        :param extension: File extension to filter to. Will be just the extension.
        :return: Nothing.
        """
        while True:
            count = 0
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    if file.rpartition(".")[2] == extension:
                        count += 1
                        print('{count}. {file}'.format(count=count, file=file))
            delete_game = input("Which game would you like to delete?\n").replace(".{ext}".format(ext=extension), "")
            try:
                os.remove("{}\\{}".format(path, delete_game))
                Loading.returning("The file was successfully deleted.", 1)
            except FileNotFoundError:
                Loading.returning("That file was not found.", 2)
            if input('Delete another file?.').lower() not in ('yes', 'sure', 'absolutely'):
                Loading.returning("Returning to the game...", 1)
                return

    @staticmethod
    def quit(self, extension: str = "."):
        """
        Method to regulate quitting and saving progress
        :param self: Game object.
        :param extension: File extension to add to the filename. Will have a . preceding it.
        :return: Nothing.
        """
        if self.new_file:
            self.filename = input("File name?\n").replace(extension, "") + extension
        try:
            game = open(self.path + "\\" + self.filename, 'w')
            game.write(Loading.caesar_encrypt(self.__repr__()))
            game.close()
            Loading.returning("Saving game progress...", 2)
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)
        return

    @staticmethod
    def open_file(path : str = "\\", filename : str = "", extension : str = ""):
        """
        Method to open files and create application objects with the proper data.
        :param path: Path to the file.
        :param filename: Filename of the file.
        :param extension: Extension of the file, used to figure out how to open a file.
        :return: An Application Object, dependent on the file extension used, and the file opened.
        """
        (filename, _, extension) = filename.rpartition('.') if not extension else extension
        try:
            file = list(open("{}\\{}".format(path, '{}.{}'.format(filename, extension)), 'r'))
            Loading.returning("Loading save file...", 1)
            file = (Loading.caesar_decrypt(file[0].replace('\n', ''))).split('(G)')
            print(file)
        except FileNotFoundError:
            Loading.returning("Choose a valid option.", 1)
            return
