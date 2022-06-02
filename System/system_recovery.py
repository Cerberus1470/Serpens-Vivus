from System import Loading
import os


class CorruptedFileSystem(Exception):
    def __init__(self, element):
        SystemRecovery.code = 0
        self.element = element


class EmptyUserFolder(Exception):
    def __init__(self, element):
        SystemRecovery.code = 1
        self.element = element


class SystemRecovery:
    code = 0

    @staticmethod
    def boot(error):
        SystemRecovery.main(SystemRecovery(error))

    def __init__(self, error):
        self.error = error
        return

    def __repr__(self):
        return

    def main(self):
        for i in range(10):
            print('\n')
        Loading.returning("Welcome to System Recovery.")
        Loading.returning("If you are here, it is because an internal error occurred and the system could not recover from it.", 5)
        if SystemRecovery.code == 0:
            self.corrupt_user()
        elif SystemRecovery.code == 1:
            self.empty_users()
        # Add more recovery codes here
        pass

    def corrupt_user(self):
        Loading.returning("In this case, the error was a corrupt user.", 3)
        Loading.returning("Here is a list of the users that are corrupted:")
        for i in list(self.error.element):
            print(i)
        Loading.returning("", len(self.error.element))
        choice = input("Would you like to learn more or delete these users?").lower()
        if choice in ("learn more", "learn", "more info", "info"):
            Loading.returning("Still in development.")
        elif choice in ("delete", "delete user", "fix the problem", "get rid of them", "destroy them all"):
            for subdir, dirs, files in os.walk("Users"):
                for i in self.error.element:
                    if i == subdir:
                        try:
                            for j in files:
                                os.remove(subdir + '\\' + j)
                            os.rmdir(subdir)
                        except OSError:
                            pass

    def empty_users(self):
        Loading.returning("In this case, the User folder is empty or contains incorrect data.", 3)
        while True:
            choice = input("Would you like to learn more or fix the issue?").lower()
            if choice in ("learn more", "learn", "more info", "info"):
                Loading.returning("This error is likely the cause of a premature termination of SETUP.", 2)
                Loading.returning("The Users Folder will be deleted and SETUP will once again occur.", 2)
                Loading.returning("Please run through setup completely.", 1)
            elif choice in ("delete", "delete folder", "delete users", "fix the issue"):
                for subdir, dirs, files in os.walk("Users"):
                    if subdir != "Users":
                        for file in files:
                            os.remove(subdir + '\\' + file)
                        os.rmdir(subdir)
                os.rmdir("Users")
                Loading.returning("The issue is fixed.")
                Loading.returning("Booting...", 2)
                return


