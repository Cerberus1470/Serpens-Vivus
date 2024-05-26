"""
Module User. Contains all the User Classes and methods within.
"""
import importlib

from System import Loading, operating_system
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
        self.username = username
        self.password = password
        self.current = current
        self.saved_state = []
        self.elevated = False
        # Saved state code!
        # FUTURE REFERENCE: Bagels, Hangman, Sonar, Sudoku, and TTT have path variables. EventViewer and SpeedSlow do not use path variables. Every other app has no saved_state.
        for i in saved_state:
            temp = [j.split(k) for j, k in ((i.split("(SS1)")[0], "(Interrupt)"), (i.split("(SS1)")[1], "(SS2)"))]
            # FUTURE REFERENCE: temp's elements are as follows: 1st list has InterruptType and Class Name. 2nd List hsa game info.
            self.saved_state.append(globals()[temp[0][0]](globals()[temp[0][1]](path, temp[1])))
        # Personalization. Defaults are shown.
        self.color = 0
        self.background = "pyidea.bg"
        self.speed = 1
        for i in personalization:
            # Color for formatting
            if i in Loading.COLORS:
                self.color = Loading.COLORS[i]
                continue
            # Backgrounds
            if i in Loading.BACKGROUNDS:
                self.background = i
                continue
            try:
                self.speed = float(i) if (i != "0" and i != "0.0") else 1.0
                continue
            except ValueError:
                continue
        return

    def __repr__(self):
        return "{}{U}{}{U}{}{U}{}{U}{}{Pe}{}{Pe}{}\n{}".format(self.__class__.__name__, self.username, self.password, str(self.current),
                                                               str(list(Loading.COLORS.keys())[list(Loading.COLORS.values()).index(self.color)]),
                                                               str(self.background), str(self.speed),
                                                               operating_system.program_separator.join(j.__repr__() for j in self.saved_state) + '\n',
                                                               U=operating_system.user_separator, Pe=operating_system.personalization_separator)
        # return "I am a user named " + self.username


class StandardUser(User):
    """
    Parent class of User that houses the code for a Standard User.
    """

    # Remove a space after a comma to reformat the file.
    def __init__(self, username="Default", password="Default", current=True, saved_state=None, personalization=None, path="\\"):
        super().__init__(username, password, current, saved_state, personalization, path)
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
