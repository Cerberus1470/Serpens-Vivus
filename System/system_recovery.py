"""
Module system_recovery. Contains every custom error class and the System Recovery app.
"""
from System import Loading
import os


class CorruptedFileSystem(Exception):
    """
    Class CorruptedFileSystem. This is an error created when the file system is detected to be corrupt.
    """
    def __init__(self, element):
        self.code = 1
        self.element = element

    def __repr__(self):
        return "The file structure is corrupted."


@DeprecationWarning
class EmptyUserFolder(Exception):
    """
    Class EmptyUserFolder. This is an error created when the user folder is empty. Recently deprecated due to changes within
    operating_system.py that prevents this from happening.
    """
    def __init__(self):
        self.code = 2

    def __repr__(self):
        return "The User folder is empty."


class NoCurrentUser(Exception):
    """
    Class NoCurrentUser. This is an error created when there is no current user.
    """
    def __init__(self):
        self.code = 3

    def __repr__(self):
        return "There is no current user."


class NoAdministrator(Exception):
    """
    Class NoAdministrator. This is an error created when there is no administrator in the system.
    """
    def __init__(self):
        self.code = 4

    def __repr__(self):
        return "There is no administrator."


class SystemRecovery:
    """
    Class SystemRecovery. This is the application to recover from fatal system crashes.
    """
    code = 0
    file = list(open("System\\recovery.info"))
    password = Loading.caesar_decrypt(file[0]).split('\t\t')[1]

    @staticmethod
    def boot(error=None):
        """
        This method regulates the startup of the System Recovery app.
        :param error: The list of errors sent from the error screen in operating_system.py.
        :return: Nothing.
        """
        if error is None:
            error = []
        Loading.log("A fatal internal error has occurred. The system has entered Recovery.")
        SystemRecovery.main(SystemRecovery(error))

    def __init__(self, error):
        self.error = error
        return

    def __repr__(self):
        return

    def main(self):
        """
        This method is the main application screen.
        :return: Nothing.
        """
        for i in range(10):
            print('\n')
        if SystemRecovery.code == 0 and not self.error:
            Loading.returning("Hey! It seems you were mistakenly sent here. There are no fatal errors to report! Have a great day.", 3)
        Loading.returning("Welcome to System Recovery.")
        Loading.returning("If you are here, it is because an internal error occurred and the system could not recover from it.", 5)
        for i in self.error:
            match i.code:
                case 1:
                    self.corrupt_user()
                case 3:
                    self.no_current_user()
                case 4:
                    self.no_admin()
            # UPDATE Add more recovery codes here
        return

    @staticmethod
    def choice(msg, responses):
        """
        This is a widely-used method to provide the user a yes or no choice based on their error.
        :param msg: Alternative choice to learning more.
        :param responses: Possible user responses to the alternative choice.
        :return: 1 if the user wants to learn more, 2 if they don't.
        """
        choice = input("Would you like to learn more or {}".format(msg)).lower()
        if choice in ("learn more", "learn", "more info", "info"):
            return 1
        elif choice in ("fix the problem", "destroy them all") or choice in responses:
            return 2
        else:
            Loading.returning("Please choose a valid option.")

    def corrupt_user(self):
        """
        This method corrects the CorruptedFileSystem error. Since these errors are only brought up when a user's info file is
        corrupt and unreadable, this is only called when a user is corrupt or unreadable.
        :return: Nothing.
        """
        Loading.returning("In this case, the error was a corrupt user.", 3)
        Loading.returning("This is the user that is corrupted:")
        cfs_count = 0
        for i in self.error:
            if i.__class__.__name__ == "CorruptedFileSystem":
                print(i.element[0])
                cfs_count += 1
        Loading.returning("", cfs_count)
        while True:
            if self.choice("delete these users?", ("delete", "delete user")) == 1:
                Loading.returning("Here is some more information on the corrupted user.", 2)
                more_info = []
                broken_separators = {}
                known_user = False
                current_stat = False
                for i in self.error:
                    if i.__class__.__name__ == "CorruptedFileSystem":
                        for j in i.element:
                            print('\t' + str(j))
                        print()
                        # Error checking the user info!
                        if i.element[1]:
                            try:
                                for j in i.element[1]:
                                    if "StandardUser" in j or "Administrator" in j or "User" in j:
                                        known_user = True
                                    if "True" in j or "False" in j:
                                        current_stat = True
                                if not known_user:
                                    more_info.append("The User is not a known type.")
                                if not current_stat:
                                    more_info.append("The current user status is not specified.")
                                if i.element[1][4] != "\n":
                                    more_info.append("There are separators missing. More info shown below.")
                                    i.element[1][4] = i.element[1][4]
                            except IndexError:
                                for j in i.element[1]:
                                    if "\t" in j:
                                        broken_separators[i.element[1].index(j)] = j
                                for j in broken_separators:
                                    while '\t' in broken_separators[j]:
                                        (one, two) = broken_separators[j].split('\t', 1)
                                        broken_separators[j] = one + '\\t' + two
                                more_info.append("The separators are broken ({}).".format(','.join(broken_separators.values())))
                        else:
                            more_info.append("The user info is not present.")
                for i in more_info:
                    Loading.returning(i, 2)
                if input("Would you like to attempt to fix these errors?").lower().startswith('y'):
                    i = 0
                    while i < len(self.error):
                        if self.error[i].__class__.__name__ == CorruptedFileSystem.__name__:
                            for j in range(1, len(self.error[i].element)):
                                for k in range(len(self.error[i].element[j])):
                                    while '\t' in self.error[i].element[j][k]:
                                        self.error[i].element[j][k] = self.error[i].element[j][k].split('\t', 1)[0] + '\\t' + self.error[i].element[j][k].split('\t', 1)[1]
                                print('\n' + str('\\t\\t'.join(self.error[i].element[j])) + '\n\tDoes this line look good? Click [ENTER] or [return] to continue or type the new line entirely, separated by "\\t\\t"s.')
                                new_element = input("Please be careful, as these changes are permanent.")
                                if new_element:
                                    while '\\t' in new_element:
                                        new_element = new_element.split('\\t', 1)[0] + '\t' + new_element.split('\\t', 1)[1]
                                    self.error[i].element[j] = (new_element + '\n').split('\t\t')
                                else:
                                    continue
                            try:
                                file = open(self.error[i].element[0] + '\\info.usr', 'w')
                                file.write(Loading.caesar_encrypt('\t\t'.join(self.error[i].element[1])))
                                file.write(Loading.caesar_encrypt('\t\t'.join(self.error[i].element[2])))
                                file.close()
                            except FileNotFoundError:
                                Loading.returning("Where did the user file go?", 3)
                                for subdir, dirs, files in os.walk("Users"):
                                    for j in self.error.element:
                                        if j == subdir:
                                            try:
                                                for k in files:
                                                    os.remove(subdir + '\\' + k)
                                                os.rmdir(subdir)
                                            except OSError:
                                                pass
                            self.error.pop(self.error.index(self.error[i]))
                            continue
                        else:
                            i += 1
                    return
            else:
                for subdir, dirs, files in os.walk("Users"):
                    for i in self.error.element:
                        if i == subdir:
                            try:
                                for j in files:
                                    os.remove(subdir + '\\' + j)
                                os.rmdir(subdir)
                            except OSError:
                                pass
                return

    @DeprecationWarning
    def empty_users(self):
        """
        This method fixes the empty user folder.
        :return:
        """
        Loading.returning("In this case, the User folder is empty or contains incorrect data.", 3)
        while True:
            if self.choice("delete the folder?", ("delete", "delete folder", "delete users", "fix the issue")) == 1:
                Loading.returning("This error is likely the cause of a premature termination of SETUP.", 2)
                Loading.returning("The Users Folder will be deleted and SETUP will once again occur.", 2)
                Loading.returning("Please run through setup completely.", 1)
            else:
                for subdir, dirs, files in os.walk("Users"):
                    if subdir != "Users":
                        for file in files:
                            os.remove(subdir + '\\' + file)
                        os.rmdir(subdir)
                os.rmdir("Users")
                Loading.returning("The issue is fixed.")
                Loading.returning("Booting...", 2)
                for i in self.error:
                    if i.__class__.__name__ == EmptyUserFolder.__name__:
                        self.error.pop(self.error.index(i))
                return

    def no_current_user(self):
        """
        This method fixes the NoCurrentUser error.
        :return:
        """
        Loading.returning("In this case, the current user was not defined, which would lead to an empty login.", 3)
        while True:
            if self.choice("set a new current user?", ("set a new", "set current user", "set a current user", "set a new current user", "continue")) == 1:
                Loading.returning("This error most likely occurred either because the current user was deleted or their user file was corrupted.", 3)
                Loading.returning("Someone may have also have externally changed a user element, causing a corrupt file or 0 current users.", 3)
            else:
                Loading.returning("\nWho should be the new current user?")
                new_current = ""
                for subdir, dirs, files in os.walk("Users"):
                    for i in dirs:
                        print(str(dirs.index(i)+1) + ". " + i)
                    while True:
                        new_current = input()
                        if new_current in dirs:
                            break
                        else:
                            Loading.returning("Please choose a valid user.", 2)
                            continue
                    break
                Loading.modify_user(new_current, 3, "True")
                Loading.returning("Setting current user...", 2)
                for i in self.error:
                    if i.__class__.__name__ == NoCurrentUser.__name__:
                        self.error.pop(self.error.index(i))
                return

    def no_admin(self):
        """
        This method fixes the NoAdministrator error.
        :return:
        """
        Loading.returning("In this case, there is no administrator on the system.", 3)
        while True:
            choice = input("Would you like to learn more, proceed with booting, or set a new admin?").lower()
            if choice in ("learn more", "learn", "more info", "info"):
                Loading.returning("This error most likely occurred either because all the administrators were deleted or their user files were corrupted.", 3)
                Loading.returning("Someone may have also have externally changed a user element, causing a corrupt file or 0 administrators.", 3)
                Loading.returning("This is not a huge problem, as many functions of the OS will still work, like games and utilities.", 3)
                Loading.returning("However, Admin functions like adding, modifying, deleting, and restoring users, resetting the system, using Task Manager, or the Event Viewer will not be available.", 5)
                Loading.returning("You may choose to continue without an admin, however the system will prompt you like this on every boot.")
            elif choice in ("new admin", "set a new", "set a new admin", "set", "set new admin", "set admin"):
                Loading.returning("\nWho should be the new administrator?")
                new_current = ""
                for subdir, dirs, files in os.walk("Users"):
                    for i in dirs:
                        print(str(dirs.index(i)+1) + ". " + i)
                    while True:
                        new_current = input()
                        if new_current in dirs:
                            break
                        else:
                            Loading.returning("Please choose a valid user.", 2)
                            continue
                    break
                if input("Enter the recovery password...") == SystemRecovery.password:
                    Loading.modify_user(new_current, 3, "True")
                    Loading.returning("Setting new Administrator...", 2)
                    for i in self.error:
                        if i.__class__.__name__ == NoAdministrator.__name__:
                            self.error.pop(self.error.index(i))
                    return
                else:
                    Loading.returning("That was not the correct password.")
                    continue
            else:
                Loading.returning("Proceeding with boot.", 2)
                for i in self.error:
                    if i.__class__.__name__ == NoAdministrator.__name__:
                        self.error.pop(self.error.index(i))
                return "override"
