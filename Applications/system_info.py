from System import Loading


class SystemInfo:

    def __init__(self):
        return

    def __repr__(self):
        return "< This is a System Info class named " + self.__class__.__name__ + ">"

    @staticmethod
    def main(versions):
        print("\nSYSTEM INFO")
        print("Software: POCS (Python Operating Command System) Version %s" % str(versions["Main"]))
        print("Shell: Python IDLE Version 3.10")
        print("Applications installed: " + str(len(versions)))
        print("Applications: Jokes, Notepad, Bagels, Tic-Tac-Toe, Task Manager, User Settings, and System Info")
        for i in range(len(versions)):
            print(list(versions)[i] + " Version: " + str(versions[list(versions)[i]]))
        if input() == "debug":
            Loading.testing()
        return

# SystemInfo.main({"main": 11.0, "jokes": 1.2, "notes": 1.3, "bagels": 1.12, "tictactoe": 1.10, "hangman": 1.8, "userset": 1.11, "sysinfo": 1.4})
