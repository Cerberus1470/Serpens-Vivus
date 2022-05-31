from Applications import bagels
from Applications import hangman
from Applications import jokes
from Applications import notepad
from Applications import sonar
from Applications import speed_up_or_slow_down
from Applications import system_info
from Applications import tictactoe
from Applications import user_settings


class User:

    def __init__(self, username="Default", password="Default", current=True, saved_state=None):

        self.username = username
        self.password = password
        self.current = current
        self.saved_state = {}
        if saved_state is None:
            self.saved_state = {bagels: "not running", hangman: "not running", jokes: "not running", notepad: "not running",
                                sonar: "not running", speed_up_or_slow_down: "not running", system_info: "not running",
                                tictactoe: "not running", user_settings: "not running"}
        else:
            apps = (bagels, hangman, jokes, notepad, sonar, speed_up_or_slow_down, system_info, tictactoe, user_settings)
            for j in apps:
                self.saved_state[j] = saved_state[apps.index(j)]

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


class Administrator(User):
    def __init__(self, username="Default", password="Default", current=True, saved_state=None):
        if saved_state == ['\n'] or not saved_state:
            super().__init__(username, password, current)
        else:
            super().__init__(username, password, current, saved_state)
        self.elevated = True
        return

    def __repr__(self):
        return "I am an administrator user named " + self.username
