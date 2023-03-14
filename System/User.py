"""
Module User. Contains all the User Classes and methods within.
"""
import importlib
import os

apps = []


#     globals()["Applications." + i.split('.')[0]] = importlib.import_module("Applications." + i.split('.')[0])
#     module_class = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules["Applications." + i.split('.')[0]])
#                     if inspect.isclass(cls_obj)]
#     print(module_class)


class User:
    """
    Class User. Child class that houses the code for a default user.
    """

    def __init__(self, username="Default", password="Default", current=True, saved_state=None, path="\\"):
        for i in [files for subdir, dirs, files in os.walk("Applications")][0]:
            if i in ("settings.py", "bruh.py"):
                continue
            name = i.split('.')[0].replace('_', ' ').title().replace(' ', '')
            globals()[name] = (importlib.__import__("Applications.{}".format(i.split('.')[0]), globals(), locals(), name)).__getattribute__(name)
            if i not in ("event_viewer.py", "task_manager.py"):
                apps.append(globals()[name])
        if saved_state is None or saved_state[0] == '':
            saved_state = []
        self.username = username
        self.password = password
        self.current = current
        self.saved_state = []
        self.elevated = False
        # FUTURE REFERENCE: Bagels, Hangman, Sonar, Sudoku, and TTT have path variables. EventViewer and SpeedSlow do not use path variables. Every other app has no saved_state.
        for i in saved_state:
            temp = [j.split(k) for j, k in ((i.split("(SS1)")[0], "(Interrupt)"), (i.split("(SS1)")[1], "(SS2)"))]
            # temp's elements are as follows: 1st list has InterruptType and Class Name. 2nd List hsa game info.
            self.saved_state.append(globals()[temp[0][0]](globals()[temp[0][1]](path, temp[1])))
            # if globals()[temp[0].split("(Interrupt)")[0]].category == "games":
            #     self.saved_state.append(globals()[temp[0].split("(Interrupt)")[0]](path, temp[1].split("(SS2)")))
            # elif globals()[temp[0].split("(Interrupt)")[0]].category == "utilities":
            #     self.saved_state.append(globals()[temp[0].split("(Interrupt)")[0]](temp[1].split("(SS2)")))
            # else:
            #     self.saved_state.append(globals()[i.split("(SS1)")[0]](i.split("(SS1)")[1]))

        # First, setting the existing program statuses.
        # for j in saved_state:
        #     if len(j) == 2:
        #         self.saved_state[globals()[j[0]]] = j[1] == "True"
        # # Now to check if any statuses are missing.
        # for n in [m for m in [k.__name__ for k in apps] if m not in [j[0] for j in saved_state]]:
        #     self.saved_state[globals()[n]] = False
        # if self.elevated:
        #     # Add more elevated apps here.
        #     for j in ("EventViewer", "TaskManager"):
        #         if j not in [k[0] for k in saved_state]:
        #             self.saved_state[globals()[j]] = False
            # if saved_state is None:
            #     self.saved_state[j] = False
            # else:
            #     self.saved_state[j] = saved_state[apps.index(j)] == "True"

        return

    def __repr__(self):
        return "I am a user named " + self.username


class StandardUser(User):
    """
    Parent class of User that houses the code for a Standard User.
    """

    # Remove a space after a comma to reformat the file.
    def __init__(self, username="Default", password="Default", current=True, saved_state=None, path="\\"):
        super().__init__(username, password, current, saved_state, path)
        # if saved_state == ['\n'] or not saved_state:
        #     super().__init__(username, password, current)
        # else:
        #     super().__init__(username, password, current, saved_state)
        return

    def __repr__(self):
        return "I am a standard user named " + self.username


# noinspection PyTypeChecker
class Administrator(User):
    """
    Parent class of User that houses the code for an Administrative User (Administrator, Admin).
    """

    def __init__(self, username="Default", password="Default", current=True, saved_state=None, path="\\"):
        super().__init__(username, password, current, saved_state, path)
        self.elevated = True
        # if saved_state == ['\n'] or not saved_state:
        #     super().__init__(username, password, current)
        # else:
        #     super().__init__(username, password, current, saved_state, True)
        # return

    def __repr__(self):
        return "I am an administrator user named " + self.username
