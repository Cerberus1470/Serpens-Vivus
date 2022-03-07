from bagels import Bagels
from tictactoe import TicTacToe
from hangman import Hangman


class User:

    def __init__(self, username, password, current, notes):
        self.username = username
        self.password = password
        self.current = current
        self.notes = notes
        self.bagels = Bagels(username, ' ', ' ', ' ', ' ', ' ')
        self.ttt = TicTacToe(username, [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ' ', ' ')
        self.hangman = Hangman(username, ' ', ' ', ' ', ' ')
        self.saved_state = {"Jokes": "not running", "Notepad": "not running", "Bagels Game": "not running",
                            "TicTacToe": "not running", "Hangman": "not running", "User Settings": "not running",
                            "System Info": "not running"}
        self.elevated = False
        return

    def __repr__(self):
        return "I am a user named " + self.username


class StandardUser(User):
    # Remove a space after a comma to reformat the file.
    def __init__(self, username, password, current, notes):
        super().__init__(username, password, current, notes)
        return

    def __repr__(self):
        return "I am a standard user named " + self.username + '\nStandardUser\t\t'


class Administrator(User):
    def __init__(self, username, password, current, notes):
        super().__init__(username, password, current, notes)
        self.elevated = True
        return

    def __repr__(self):
        return "I am an administrator user named " + self.username + '\nAdministrator\t\t'
