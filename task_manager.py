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
        print("The Jokes program is " + stats["Jokes"] + ". Type 'jquit' to quit the jokes program.")
        print("The Notes program is " + stats["Notepad"] + ". Type 'nquit' to quit the notes program.")
        print("The Bagels program is " + stats["Bagels Game"] + ". Type 'bquit' to quit the bagels program.")
        print("The Tic-Tac-Toe program is " + stats["TicTacToe"] + ". Type 'tquit' to quit the tic-tac-toe program.")
        print("The User Settings program is " + stats["User Settings"] + ". Type 'uquit' to quit the user settings program.")
        print("The System Info program is " + stats["System Info"] + ". Type 'squit' to quit the system info program.")
        while True:
            print("\nType any of the commands above to quit the corresponding programs or type 'quitall' to quit all "
                  "programs! All progress will be erased if the programs are quit. To save progress, go into the app "
                  "and save your progress there. Otherwise, just press [ENTER] or [return] to return to the applications "
                  "screen!")
            quit_choice = input()
            if quit_choice == 'jquit':
                stats["Jokes"] = "not running"
                print("The Jokes Program was successfully quit.")
            elif quit_choice == 'nquit':
                stats["Notepad"] = "not running"
                print("The Notes Program was successfully quit.")
            elif quit_choice == 'bquit':
                stats["Bagels Game"] = "not running"
                print("The Bagels Program was successfully quit.")
            elif quit_choice == 'tquit':
                stats["TicTacToe"] = "not running"
                print("The Tic-Tac-Toe Program was successfully quit.")
            elif quit_choice == 'uquit':
                stats["User Settings"] = "not running"
                print("The User Settings Program was successfully quit.")
            elif quit_choice == 'squit':
                stats["System Info"] = "not running"
                print("The System Info Program was successfully quit.")
            elif quit_choice == 'quitall':
                stats["Jokes"] = stats["Notepad"] = stats["Bagels Game"] = stats["TicTacToe"] = stats["User Settings"] = stats[
                    "System Info"] = "not running"
                print("All programs were successfully quit.")
            else:
                break
