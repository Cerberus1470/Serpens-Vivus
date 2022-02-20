class User:
    # Remove a space after a comma to reformat the file.

    def __init__(self, username, password, current, notes):
        self.username = username
        self.password = password
        self.current = current
        self.notes = notes
        return

    def __repr__(self):
        return "I am a user named " + self.username

    def __setGames__(self, bagels_game, ttt_game, hangman_game, state):
        self.bagels = bagels_game
        self.ttt = ttt_game
        self.hangman = hangman_game
        self.saved_state = state
        return
