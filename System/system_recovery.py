from System import Loading
import os


def boot(code, dirty):
    SystemRecovery.main(SystemRecovery(dirty), code)


class SystemRecovery:
    def __init__(self, dirty):
        self.dirty = dirty
        return

    def __repr__(self):
        return

    def main(self, code):
        for i in range(10):
            print('\n')
        Loading.returning("Welcome to System Recovery. If you are here, it is because an internal error occurred and the system could not recover from it.", 5)
        if code == 0:
            self.corrupt_user()
        # Add more recovery codes here
        pass

    def corrupt_user(self):
        Loading.returning("In this case, the error was a corrupt user.", 3)
        Loading.returning("Here is a list of the users that are corrupted:")
        for i in self.dirty:
            print(i)
        Loading.returning("", len(self.dirty))
        choice = input("Would you like to learn more or delete these users?").lower()
        if choice in ("learn more", "learn", "more info", "info"):
            Loading.returning("Still in development.")
        elif choice in ("delete", "delete user", "fix the problem", "get rid of them", "destroy them all"):
            for subdir, dirs, files in os.walk("Users"):
                for i in self.dirty:
                    if i == subdir:
                        try:
                            for j in files:
                                os.remove(subdir + '\\' + j)
                            os.rmdir(subdir)
                        except OSError:
                            pass
