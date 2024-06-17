"""
Module Console. System application that mimics Command Prompt or Terminal
"""
from Applications.task_manager import TaskManager

category = "utilities"
version = "1.0"
entries = ("console", "terminal", "command prompt", "prompt", "python")


def boot(os_object=None):
    """
    Method to regulate startup of the console.
    :param os_object: The OperatingSystem object, used for the saved state in case the user kills a process from here.
    :return: Nothing
    """
    Console.main(os_object)


class Console:
    """
    Class Console. Houses the main application for the python console.
    """
    def __init__(self):
        pass

    def __repr__(self):
        pass

    @staticmethod
    def main(os_object):
        """
        The main method for the Python Console.
        :return: Nothing.
        """
        import sys, traceback
        print("Python {version} on {platform}".format(version=sys.version, platform=sys.platform))
        while True:
            command = input(">>> ")
            if command.partition(" ")[0] in ("kill", "taskkill"):
                TaskManager.kill(command.partition(" ")[2], os_object.current_user.saved_state)
            try:
                exec(command)
            except SystemExit:
                return
            except Exception as error:
                traceback.print_exception(error)
