from Applications.task_manager import TaskManager
from Applications.event_viewer import EventViewer
from Applications.jokes import Jokes
from Applications.notepad import Notepad
from Applications.speed_up_or_slow_down import SpeedSlow
from Applications.bagels import Bagels
from Applications.tictactoe import TicTacToe
from Applications.hangman import Hangman
from Applications.sonar import Sonar
from Applications.scout_rpg import ScoutRPG
from Applications.system_info import SystemInfo
from Applications.user_settings import UserSettings


class User:

    def __init__(self, username="Default", password="Default", current=True, saved_state=None):

        self.username = username
        self.password = password
        self.current = current
        self.saved_state = {}
        # Alphabetical order
        apps = (Bagels, Hangman, Jokes, Notepad, ScoutRPG, Sonar, SpeedSlow, SystemInfo, TicTacToe, UserSettings)
        for j in apps:
            if saved_state is None:
                self.saved_state[j] = False
            else:
                self.saved_state[j] = saved_state[apps.index(j)] == "True"

        self.elevated = False
        return

    def __repr__(self):
        return "I am a user named " + self.username


class StandardUser(User):
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
    def __init__(self, username="Default", password="Default", current=True, saved_state=None):
        if saved_state == ['\n'] or not saved_state:
            super().__init__(username, password, current)
            self.saved_state[EventViewer] = False
            self.saved_state[TaskManager] = False
        else:
            super().__init__(username, password, current, saved_state)
            self.saved_state[EventViewer] = saved_state[9] == "True"
            self.saved_state[TaskManager] = saved_state[10] == "True"
        self.elevated = True
        return

    def __repr__(self):
        return "I am an administrator user named " + self.username
