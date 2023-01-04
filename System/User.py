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

    def __init__(self, username="Default", password="Default", current=True, saved_state=None, elevation=False):
        for i in [files for subdir, dirs, files in os.walk("Applications")][0]:
            if i in ("settings.py", "bruh.py"):
                continue
            name = i.split('.')[0].replace('_', ' ').title().replace(' ', '')
            globals()[name] = (importlib.__import__("Applications.{}".format(i.split('.')[0]), globals(), locals(), name)).__getattribute__(name)
            if i not in ("event_viewer.py", "task_manager.py"):
                apps.append(globals()[name])
        if saved_state is None:
            saved_state = {}
        self.username = username
        self.password = password
        self.current = current
        self.saved_state = {}
        self.elevated = elevation
        # First, setting the existing program statuses.
        for j in saved_state:
            if len(j) == 2:
                self.saved_state[globals()[j[0]]] = j[1] == "True"
        # Now to check if any statuses are missing.
        for n in [m for m in [k.__name__ for k in apps] if m not in [j[0] for j in saved_state]]:
            self.saved_state[globals()[n]] = False
        if self.elevated:
            # Add more elevated apps here.
            for j in ("EventViewer", "TaskManager"):
                if j not in [k[0] for k in saved_state]:
                    self.saved_state[globals()[j]] = False
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
    def __init__(self, username="Default", password="Default", current=True, saved_state=None):
        if saved_state == ['\n'] or not saved_state:
            super().__init__(username, password, current)
        else:
            super().__init__(username, password, current, saved_state)
        return

    def __repr__(self):
        return "I am a standard user named " + self.username


# noinspection PyTypeChecker
class Administrator(User):
    """
    Parent class of User that houses the code for an Administrative User (Administrator, Admin).
    """

    def __init__(self, username="Default", password="Default", current=True, saved_state=None):
        self.elevated = True
        if saved_state == ['\n'] or not saved_state:
            super().__init__(username, password, current)
        else:
            super().__init__(username, password, current, saved_state, True)
        return

    def __repr__(self):
        return "I am an administrator user named " + self.username
