"""
Module system_recovery. Contains every custom error class and the System Recovery app.
"""
import shutil

import pynput.keyboard

from System import Loading, operating_system
import os


class CorruptedFileSystem(Exception):
    """
    Class CorruptedFileSystem. This is an error created when the file system is detected to be corrupt.
    """

    def __init__(self, subdir : str = "\\", info : list = None, person : list = None, programs : list = None, element : list = None):
        self.code = 1
        self.subdir = subdir
        self.info = info
        self.person = person
        self.programs = programs
        self.element = element if element else [subdir, info, person, programs]
        self.args = (self.__repr__(),)

    def __repr__(self):
        return "The file structure is corrupted."


@DeprecationWarning
class NoCurrentUser(Exception):
    """
    Class NoCurrentUser. This is an error created when there is no current user.
    """

    def __init__(self):
        self.code = 3
        self.args = (self.__repr__(),)

    def __repr__(self):
        return "There is no current user."


class NoAdministrator(Exception):
    """
    Class NoAdministrator. This is an error created when there is no administrator in the system.
    """

    def __init__(self):
        self.code = 4
        self.args = (self.__repr__(),)

    def __repr__(self):
        return "There is no administrator."


class CorruptedRegistry(Exception):
    """
    Class CorruptedRegistry. This is an error created when a registry key is missing.
    """

    def __init__(self, registry):
        self.code = 5
        self.element = registry
        self.args = (self.__repr__(),)

    def __repr__(self):
        return "The Registry is corrupted or missing files."


password = Loading.caesar_decrypt(list(open("System\\REGISTRY\\SVKEY_SYSTEM\\Recovery.svkey"))[0])


def boot(error=None):
    """
    This method regulates the startup of the System Recovery app.
    :param error: The list of errors sent from the error screen in operating_system.py.
    :return: Nothing.
    """
    Loading.returning("Entering Recovery...", 1)
    if error is None:
        error = []
    Loading.log("A fatal internal error has occurred. The system has entered Recovery.")
    SystemRecovery.main(SystemRecovery(error))
    Loading.returning("Saving changes and booting...", 3)
    print('\n\n\n\n\n')


class SystemRecovery:
    """
    Class SystemRecovery. This is the application to recover from fatal system crashes.
    """

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
        if self.error:
            Loading.returning("Welcome to System Recovery.\nIf you are here, it is because an internal error occurred and the system could not recover from it.", 5)
            for i in self.error:
                match i.code:
                    case 1:
                        self.corrupt_user()
                    case 4:
                        self.no_admin()
                    case 5:
                        self.corrupt_registry()
                # UPDATE Add more recovery codes here
        else:
            Loading.returning("Hey! It seems you were mistakenly sent here. There are no fatal errors to report! Have a great day.", 3)
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
        Loading.returning("In this case, the error was a corrupt user. Here are the corrupted user(s):\n{}".format(
            ", ".join(i.subdir for i in self.error if i.__class__ == CorruptedFileSystem)), 3)
        while True:
            if self.choice("delete these users?", ("delete", "delete user")) == 1:
                Loading.returning("Here is some more information on the corrupted user.", 2)
                print('\n'.join('\t' + str(j) for i in self.error if i.__class__ == CorruptedFileSystem for j in i.element[1:]))
                more_info = []
                for i in self.error:
                    if i.__class__ == CorruptedFileSystem and i.info:
                        try:
                            known_user = any(["StandardUser" in j or "Administrator" in j or "User" in j for j in i.info])
                            current_stat = any(["True" in j or "False" in j for j in i.info])
                            if not known_user:
                                more_info.append("The User is not a known type.")
                            if not current_stat:
                                more_info.append("The current user status is not specified.")
                            if i.info[4] != "\n":
                                more_info.append("There are separators missing. More info shown below.")
                                i.info[4] = i.info[4]
                        except IndexError:
                            broken_separators = {i.info.index(j): j.replace('\t', '\\t') for j in i.info if operating_system.user_separator in j}
                            # for j in i.info:
                            #     if "\t" in j:
                            #         broken_separators[i.info.index(j)] = j
                            # for j in broken_separators:
                            #     while '\t' in broken_separators[j]:
                            #         (one, two) = broken_separators[j].split('\t', 1)
                            #         broken_separators[j] = one + '\\t' + two
                            more_info.append("The separators are broken ({}).".format(','.join(broken_separators.values())))
                    if not more_info:
                        more_info.append("The user info is not present.")
                for i in more_info:
                    Loading.returning(i, 2)
                if input("Would you like to attempt to fix these errors?").lower().startswith('y'):
                    Loading.returning("Each line of the user info file will be printed.\nYou can correct the errors by editing the text and tapping [ENTER] or [return].", 3)
                    for i in self.error:
                        if i.__class__ == CorruptedFileSystem and i.element:
                            pynput.keyboard.Controller().type(operating_system.user_separator.join(i.info))  # First the user info
                            i.info = input("Please make sure the line is correct. These changes are permanent.\nEdit your changes and then tap [ENTER] or [return].\n")
                            pynput.keyboard.Controller().type(operating_system.personalization_separator.join(i.person))  # First the user info
                            i.person = input("Please make sure the line is correct. These changes are permanent.\nEdit your changes and then tap [ENTER] or [return].\n")
                            pynput.keyboard.Controller().type(operating_system.program_separator.join(i.programs))  # First the user info
                            i.programs = input("Please make sure the line is correct. These changes are permanent.\nEdit your changes and then tap [ENTER] or [return].\n")
                            try:
                                open("{subdir}\\info.usr".format(subdir=i.subdir), 'w').write('\n'.join([i.info, i.person, i.programs]))
                                Loading.progress_bar("Recovery will now write the changes to the disk.", (len(i.info) + len(i.person) + len(i.programs)) / 50)
                                Loading.returning("Recovery has successfully written the changes to disk.", 2)
                            except (FileNotFoundError, FileExistsError, OSError):
                                Loading.returning("Recovery was unable to write the changes to disk.", 2)
                    # i = 0
                    # while i < len(self.error):
                    #     if self.error[i].__class__ == CorruptedFileSystem:
                    #         for j in range(1, len(self.error[i].element)):
                    #             for k in range(len(self.error[i].element[j])):
                    #                 while '\t' in self.error[i].element[j][k]:
                    #                     self.error[i].element[j][k] = self.error[i].element[j][k].split('\t', 1)[0] + '\\t' + self.error[i].element[j][k].split('\t', 1)[1]
                    #             print('\n' + str('\\t\\t'.join(self.error[i].element[j])) + '\n\tDoes this line look good? Click [ENTER] or [return] to continue or type the new line entirely, separated by "\\t\\t"s.')
                    #             new_element = input("Please be careful, as these changes are permanent.")
                    #             if new_element:
                    #                 while '\\t' in new_element:
                    #                     new_element = new_element.split('\\t', 1)[0] + '\t' + new_element.split('\\t', 1)[1]
                    #                 self.error[i].element[j] = (new_element + '\n').split('\t\t')
                    #             else:
                    #                 continue
                    #         try:
                    #             file = open(self.error[i].subdir + '\\info.usr', 'w')
                    #             file.write(Loading.caesar_encrypt('\t\t'.join(self.error[i].info)))
                    #             file.write(Loading.caesar_encrypt('\t\t'.join(self.error[i].element[2])))
                    #             file.close()
                    #         except FileNotFoundError:
                    #             Loading.returning("Where did the user file go?", 3)
                    #             for subdir, dirs, files in os.walk("Users"):
                    #                 for j in self.error.element:
                    #                     if j == subdir:
                    #                         try:
                    #                             for k in files:
                    #                                 os.remove(subdir + '\\' + k)
                    #                             os.rmdir(subdir)
                    #                         except OSError:
                    #                             pass
                    #         self.error.pop(self.error.index(self.error[i]))
                    #         continue
                    #     else:
                    #         i += 1
                    # return
            else:
                for i in self.error:
                    if i.__class__ == CorruptedFileSystem:
                        try:
                            shutil.rmtree(i.subdir)
                        except (shutil.Error, FileExistsError, FileNotFoundError, OSError):
                            Loading.returning("Recovery was unable to delete the user folder.", 2)
                # for subdir, dirs, files in os.walk("Users"):
                #     for i in self.error.element:
                #         if i == subdir:
                #             try:
                #                 for j in files:
                #                     os.remove(subdir + '\\' + j)
                #                 os.rmdir(subdir)
                #             except OSError:
                #                 pass
            return

    @DeprecationWarning
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
                        print(str(dirs.index(i) + 1) + ". " + i)
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
                continue
            elif choice in ("set a new admin", "set a new", "set an admin", "set new admin", "set new", "set admin", "new admin", "set", "new", "admin"):
                Loading.returning("\nWho should be the new administrator?")
                print('\n'.join("{}. {}".format(dirs.index(i) + 1, i) for _, dirs, _ in os.walk("Users") for i in dirs))
                new_current = input()
                if new_current not in [dirs for _, dirs, _ in os.walk("Users") for dirs in dirs]:
                    Loading.returning("Please choose a valid user.", 2)
                # for subdir, dirs, files in os.walk("Users"):
                #     for i in dirs:
                #         print(str(dirs.index(i) + 1) + ". " + i)
                #     while True:
                #         new_current = input()
                #         if new_current in dirs:
                #             break
                #         else:
                #             Loading.returning("Please choose a valid user.", 2)
                #             continue
                #     break
                if input("Enter the recovery password...") == password:
                    Loading.modify_user(new_current, 0, "Administrator")
                    Loading.returning("Setting new Administrator...", 2)
                    break
                else:
                    Loading.returning("That was not the correct password.")
                    continue
            Loading.returning("Proceeding with boot.", 2)
            for i in self.error:
                if i.__class__ == NoAdministrator:
                    self.error.pop(self.error.index(i))
            return

    def corrupt_registry(self):
        pass
