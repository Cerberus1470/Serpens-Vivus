"""
Module task_manager. This module contains the application TaskManager to monitor and quit running processes
inside the OS.
"""
import sys
from System import Loading


category = "admin"
version = "2.0_alpha01"
entries = ('task manager', '7')


def boot(os_object=None):
    """
    This method manages and regulates the boot process.
    :param os_object: The Cerberus OS Object.
    :return: Nothing.
    """
    TaskManager.main(os_object.current_user.saved_state)


class TaskManager:
    """
    Class TaskManager. This class contains the application.
    """

    def __init__(self):
        return

    def __repr__(self):
        return "< This is a Task Manager class named " + self.__class__.__name__ + ">"

    @staticmethod
    def quit(app, stats):
        """
        This method quits programs.
        :param app: The app to quit.
        :param stats: The dictionary of process statuses.
        :return: Nothing.
        """
        if app == 'quitall':
            stats["Jokes"] = stats["Notepad"] = stats["Bagels Game"] = stats["Tictactoe"] = stats["User Settings"] = \
                stats["System Info"] = "not running"
            pass
        else:
            stats[str(app)] = 'not running'
            print("The " + str(app) + " Program was successfully quit.")

    @staticmethod
    def main(saved_state):
        """
        The main application method to view and quit processes.
        :param saved_state: The list of Interrupt objects.
        :return: Nothing.
        """
        while True:
            print("\nWelcome to the task manager!\nHere you will find all the programs currently running. Quitting them will result in lost progress.\n")
            if not saved_state:
                print("There are no processes running.")
            else:
                print("\n".join(["Process name\tSize\t\tReferences\n{}\t\t\t{}\t\t\t{}".format(
                    i.args[0].__class__.__name__.title(), sys.getsizeof(i.args[0]), sys.getrefcount(i.args[0])-1) for i in saved_state]))
            quit_choice = input("Which application do you want to force-quit?").lower()
            if quit_choice in ("", "exit", "quit", "get me outta here"):
                return
            TaskManager.kill(quit_choice, saved_state)
        # for i in stats:
        #     print("The {} program is {}.".format(i.__name__, "running" if stats[i] else "not running"))
        # # print("The Jokes program is {}.")
        # # print("The Bagels program is {}.")
        # # print("The Tic-Tac-Toe program is {}.")
        # # print("The Hangman program is {}.")
        # # print("The Sonar program is {}.")
        # # print("The SpeedSlow program is {}.")
        # # print("The Notes program is " + stats[Notepad] + ".")
        # # print("The User Settings program is " + stats[UserSettings] + ".")
        # # print("The System Info program is " + stats[SystemInfo] + ".")
        # # if elevation:
        # #     print("The Task Manager program is " + stats[TaskManager] + ".")
        # #     print("The Event Viewer program is " + stats[EventViewer] + ".")
        # while True:
        #     print('\nType "quit" and the app you want to quit (i.e. "quit jokes") or type "quitall" to quit all programs!'
        #           '\nPress [ENTER] or [return] to return to the applications screen!')
        #     quit_choice = input().lower()[5:]
        #     if quit_choice == 'jokes':
        #         stats["Jokes"] = "not running"
        #         print("The Jokes Program was successfully quit.")
        #     elif quit_choice == 'notes':
        #         stats["Notepad"] = "not running"
        #         print("The Notes Program was successfully quit.")
        #     elif quit_choice == 'bagels':
        #         stats["Bagels Game"] = "not running"
        #         print("The Bagels Program was successfully quit.")
        #     elif quit_choice == 'tic-tac-toe':
        #         stats["Tictactoe"] = "not running"
        #         print("The Tic-Tac-Toe Program was successfully quit.")
        #     elif quit_choice == 'user settings':
        #         stats["User Settings"] = "not running"
        #         print("The User Settings Program was successfully quit.")
        #     elif quit_choice == 'system info':
        #         stats["System Info"] = "not running"
        #         print("The System Info Program was successfully quit.")
        #     elif quit_choice == 'quitall':
        #         stats["Jokes"] = stats["Notepad"] = stats["Bagels Game"] = stats["Tictactoe"] = stats["User Settings"] = stats[
        #             "System Info"] = "not running"
        #         print("All programs were successfully quit.")
        #     else:
        #         Loading.returning_to_apps()
        #         break
        # return

    @staticmethod
    def kill(quit_choice, saved_state):
        """
        Method to kill a process based on a user input and a saved_state dictionary.
        :param quit_choice:
        :param saved_state:
        """
        if quit_choice in [i.args[0].__class__.__name__.lower() for i in saved_state]:
            try:
                saved_state.pop([i.args[0].__class__.__name__.lower() for i in saved_state].index(quit_choice))
            except ValueError:
                Loading.returning("The OS failed to quit the process.", 2)
        else:
            Loading.returning("That is not a valid process.")
