class User:
    # Remove a space after a comma to reformat the file.

    def __init__(self, username, password, current, notes):
        self.username = username
        self.password = password
        self.current = current
        self.notes = notes
        self.bagels = ''
        self.ttt = ''
        self.hangman = ''
        self.saved_state = ''
        return

    def __repr__(self):
        return "I am a user named " + self.username
