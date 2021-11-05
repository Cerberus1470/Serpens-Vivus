class SysInfo:
    def __init__(self):
        return

    def __repr__(self):
        return "< This is a System Info class named " + self.__class__.__name__ + ">"

    def main(self, stats, versions):
        stats["System Info"] = "running"
        print("\nSYSTEM INFO")
        print("Software: POCS (Python Operating Command System) Version %s" % (versions["main"]))
        print("Shell: Python IDLE Version 3.10")
        print("Applications installed: 6")
        print("Applications: Jokes, Notepad, Bagels, Tic-Tac-Toe, Task Manager, User Settings, and System Info")
        print("Jokes Version: %s" % versions["jokes"])
        print("Notepad Version: %s" % versions["notes"])
        print("Bagels Version: %s" % versions["bagels"])
        print("Tic-Tac-Toe Version: %s" % versions["tictactoe"])
        print("User Settings Version: %s" % versions["userset"])
        print("System Info Version: %s" % versions["sysinfo"])
        print("Press [ENTER] or [return] to return to the applications screen!")
        input()
        return
