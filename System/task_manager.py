from System import Loading

category = "admin"


def boot(os_object):
    TaskManager.main(os_object.current_user.saved_state)


class TaskManager:
    def __init__(self):
        return

    def __repr__(self):
        return "< This is a Task Manager class named " + self.__class__.__name__ + ">"

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
    def main(stats):
        print()
        print("Welcome to the task manager!")
        print("Here you will find all the programs currently running. You are also able to quit them, however it "
              "clears no memory space, and all program memory will be saved (such as notes).")
        print("The Jokes program is " + stats["Jokes"] + ".")
        print("The Notes program is " + stats["Notepad"] + ".")
        print("The Bagels program is " + stats["Bagels Game"] + ".")
        print("The Tic-Tac-Toe program is " + stats["TicTacToe"] + ".")
        print("The User Settings program is " + stats["User Settings"] + ".")
        print("The System Info program is " + stats["System Info"] + ".")
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
