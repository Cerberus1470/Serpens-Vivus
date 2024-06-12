"""
Module system_info. Houses the application.
"""
from System import Loading, operating_system
import os
import importlib


category = "utilities"
version = "1.0.12"
entries = ('system info', 'sys info', '9')


def boot(os_object=None):
    """
    This method regulates the boot sequence of this application.
    :return: Nothing.
    """
    apps = []
    for file in [files for subdir, dirs, files in os.walk("Applications")][0]:
        apps.append(importlib.import_module("Applications.{}".format(file.replace(".py", ""))))
    SystemInfo.main(apps, os_object)


class SystemInfo:
    """
    Class SystemInfo. Houses the main application.
    """

    def __init__(self):
        return

    def __repr__(self):
        return "< This is a System Info class named " + self.__class__.__name__ + ">"

    @staticmethod
    def main(apps=None, os_object=None):
        """
        The main application screen.
        :param apps: The list of apps in the Applications folder.
        :param os_object: The OperatingSystem object, used for the version.
        :return:
        """
        print("\nSYSTEM INFO")
        print("Software: POCS (Python Operating Command System) Version {}".format(str(operating_system.version)))
        print("Shell: Python Version {}".format(os_object.registry.get_key("Shell")))
        print("Applications installed: " + str(len(apps)))
        print("Applications: " + ', '.join([i.__name__.replace("_", "").title() for i in apps]))
        for i in apps:
            print("{app} Version: {version}".format(app=i.__name__.replace("_", "").title(), version=i.version))
        if Loading.pocs_input() == "debug":
            Loading.returning("")
        return

# SystemInfo.main({"main": 11.0, "jokes": 1.2, "notes": 1.3, "bagels": 1.12, "tictactoe": 1.10, "hangman": 1.8, "user_set": 1.11, "sysinfo": 1.4})
