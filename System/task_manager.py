from System import Loading
from System.event_viewer import EventViewer
from Applications.jokes import Jokes
from Applications.notepad import Notepad
from Applications.speed_up_or_slow_down import SpeedSlow
from Applications.bagels import Bagels
from Applications.tictactoe import TicTacToe
from Applications.hangman import Hangman
from Applications.sonar import Sonar
from Applications.system_info import SystemInfo
from Applications.user_settings import UserSettings


class TaskManager:
    category = "admin"
    name = "Task Manager"

    @staticmethod
    def boot(os_object):
        TaskManager.main(os_object.current_user.saved_state, os_object.current_user.elevated)

    def __init__(self):
        return

    def __repr__(self):
        return "Task Manager"

    @staticmethod
    def quit(app, stats):
        if app == 'quitall':
            stats["Jokes"] = stats["Notepad"] = stats["Bagels Game"] = stats["TicTacToe"] = stats["User Settings"] = \
                stats["System Info"] = "not running"
            pass
        else:
            stats[str(app)] = 'not running'
            print("The " + str(app) + " Program was successfully quit.")

    @staticmethod
    def main(stats, elevation):
        print()
        print("Welcome to the task manager!")
        print("Here you will find all the programs currently running. You are also able to quit them, however it "
              "clears no memory space, and all program memory will be saved (such as notes).")
        print("The Jokes program is " + stats[Jokes] + ".")
        print("The Bagels program is " + stats[Bagels] + ".")
        print("The Tic-Tac-Toe program is " + stats[TicTacToe] + ".")
        print("The Hangman program is " + stats[Hangman] + ".")
        print("The Sonar program is " + stats[Sonar] + ".")
        print("The SpeedSlow program is " + stats[SpeedSlow] + ".")
        print("The Notes program is " + stats[Notepad] + ".")
        print("The User Settings program is " + stats[UserSettings] + ".")
        print("The System Info program is " + stats[SystemInfo] + ".")
        if elevation:
            print("The Task Manager program is " + stats[TaskManager] + ".")
            print("The Event Viewer program is " + stats[EventViewer] + ".")
        while True:
            print('\nType "quit" and the app you want to quit (i.e. "quit jokes") or type "quitall" to quit all programs!'
                  '\nPress [ENTER] or [return] to return to the applications screen!')
            quit_choice = input().lower()[5:]
            if quit_choice == 'jokes':
                stats["Jokes"] = "not running"
                print("The Jokes Program was successfully quit.")
            elif quit_choice == 'notes':
                stats["Notepad"] = "not running"
                print("The Notes Program was successfully quit.")
            elif quit_choice == 'bagels':
                stats["Bagels Game"] = "not running"
                print("The Bagels Program was successfully quit.")
            elif quit_choice == 'tic-tac-toe':
                stats["TicTacToe"] = "not running"
                print("The Tic-Tac-Toe Program was successfully quit.")
            elif quit_choice == 'user settings':
                stats["User Settings"] = "not running"
                print("The User Settings Program was successfully quit.")
            elif quit_choice == 'system info':
                stats["System Info"] = "not running"
                print("The System Info Program was successfully quit.")
            elif quit_choice == 'quitall':
                stats["Jokes"] = stats["Notepad"] = stats["Bagels Game"] = stats["TicTacToe"] = stats["User Settings"] = stats[
                    "System Info"] = "not running"
                print("All programs were successfully quit.")
            else:
                Loading.returning_to_apps()
                break
