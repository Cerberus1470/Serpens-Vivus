"""
Module system_info. Houses the application.
"""
from System import Loading


class SystemInfo:
    """
    Class SystemInfo. Houses the main application.
    """
    category = "utilities"

    @staticmethod
    def boot(os_object):
        """
        This method regulates the boot sequence of this application.
        :param os_object: The Cerberus OS object.
        :return: Nothing.
        """
        SystemInfo.main(os_object.versions)

    def __init__(self):
        return

    def __repr__(self):
        return "< This is a System Info class named " + self.__class__.__name__ + ">"

    @staticmethod
    def main(versions):
        """
        The main application screen.
        :param versions:
        :return:
        """
        print("\nSYSTEM INFO")
        print("Software: POCS (Python Operating Command System) Version %s" % str(versions["Main"]))
        print("Shell: Python IDLE Version 3.10")
        print("Applications installed: " + str(len(versions)))
        print("Applications: " + str(versions.keys()))
        for i in range(len(versions)):
            print(list(versions)[i] + " Version: " + str(versions[list(versions)[i]]))
        if input() == "debug":
            Loading.returning("")
        return

# SystemInfo.main({"main": 11.0, "jokes": 1.2, "notes": 1.3, "bagels": 1.12, "tictactoe": 1.10, "hangman": 1.8, "user_set": 1.11, "sysinfo": 1.4})
