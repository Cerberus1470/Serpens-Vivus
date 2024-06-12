"""
Module User. Contains all the User Classes and methods within.
"""
import importlib

from System import operating_system
from System.Loading import *

apps = []


class User:
    """
    Class User. Child class that houses the code for a default user.
    """

    def __init__(self, username="Default", password="Default", current=True, saved_state=None, personalization=None, path="\\"):
        if personalization is None:
            personalization = []
        for i in [files for subdir, dirs, files in os.walk("Applications")][0]:
            if i in ("settings.py", "bruh.py"):
                continue
            name = i.split('.')[0].replace('_', ' ').title().replace(' ', '')
            globals()[name] = (importlib.__import__("Applications.{}".format(i.split('.')[0]), globals(), locals(), name)).__getattribute__(name)
            if i not in ("event_viewer.py", "task_manager.py"):
                apps.append(globals()[name])
        # Defaults for everything.
        if saved_state is None or saved_state[0] == '':
            saved_state = []
        if username.__class__ == list:
            self.username = username[0]
            self.password = username[1]
            self.current = username[2] == 'True'
        else:
            self.username = username
            self.password = password
            self.current = current
        self.saved_state = []
        # Saved state code!
        # FUTURE REFERENCE: Bagels, Hangman, Sonar, Sudoku, and TTT have path variables. EventViewer and SpeedSlow do not use path variables. Every other app has no saved_state.
        for i in saved_state:
            temp = [j.split(k) for j, k in ((i.split("(SS1)")[0], "(Interrupt)"), (i.split("(SS1)")[1], "(SS2)"))]
            # FUTURE REFERENCE: temp's elements are as follows: 1st list has InterruptType and Class Name. 2nd List hsa game info.
            self.saved_state.append(globals()[temp[0][0]](globals()[temp[0][1]](path, temp[1])))
        # Personalization. Defaults are shown.
        if personalization:
            self.color = int(personalization[0])
            self.background = personalization[1]
            self.taskbar = personalization[2].split(",")
        else:
            self.color = 0
            self.background = "pyidea.bg"
            self.taskbar = ["Notepad", "Settings"]
        return

    def __repr__(self):
        return "{tp}{U}{un}{U}{pw}{U}{cu}\n{co}{Pe}{bg}{Pe}{tb}\n{ss}\n".format(
            tp=self.__class__.__name__, un=self.username, pw=self.password, cu=str(self.current),
            co=str(self.color), bg=self.background, tb=','.join(self.taskbar),
            ss=operating_system.program_separator.join(i.__repr__() for i in self.saved_state),
            U=operating_system.user_separator, Pe=operating_system.personalization_separator)


class StandardUser(User):
    """
    Parent class of User that houses the code for a Standard User.
    """

    # Remove a space after a comma to reformat the file.
    def __init__(self, username="Default", password="Default", current=True, saved_state=None, personalization=None, path="\\"):
        super().__init__(username, password, current, saved_state, personalization, path)
        self.elevated = False
        return


# noinspection PyTypeChecker
class Administrator(User):
    """
    Parent class of User that houses the code for an Administrative User (Administrator, Admin).
    """

    def __init__(self, username="Default", password="Default", current=True, saved_state=None, personalization=None, path="\\"):
        super().__init__(username, password, current, saved_state, personalization, path)
        self.elevated = True
        return
