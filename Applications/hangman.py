# This program is a game of hangman! It will randomly select a word from 4 different categories, displays what category was chosen, and gives the player 5 incorrect guesses before the potato man is hung. Dark, I know right? The fate of a man lies in
# your ability to guess a word. Good luck! Side note: I thought we were supposed to have a working program, so I just fixed the broken code. Everything works :)
import os
from System import Loading
import random
from Applications import bagels


HANGMAN_PICS = ['''
  +-----+
  |     |
  |     |
        |
        |
        |
        |
        |
=========''', '''

  +-----+
  |     |
  O     |
        |
        |
        |
        |
        |
=========''', '''

  +-----+
  |     |
  O     |
  |     |
  |     |
        |
        |
        |
=========''', '''

  +-----+
  |     |
  O     |
/ |     |
  |     |
        |
        |
        |
=========''', '''

  +-----+
  |     |
  O     |
/ | \   |
  |     |
        |
        |
        |
=========''', '''

  +-----+
  |     |
  O     |
/ | \   |
  |    |
 /      |
        |
        |
=========''', '''

  +-----+
  |     |
  O     |
/ | \   |
  |     |
 / \    |
        |
        |
=========''']
words = {  # this is the word bank
    'Colors': 'red orange yellow green blue indigo violet white black brown'.split(),
    'Shapes': 'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon heptagon octagon'.split(),
    'Fruits': 'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
    'Animals': 'bat bear beaver cat cougar crab deer dog donkey duck eagle fish frog goat leech lion lizard monkey moose mouse otter owl panda python rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale wolf wombat zebra'.split()}


class Hangman:
    category = "games"
    name = "Hangman"

    @staticmethod
    def boot(path="\\"):
        hangman = Hangman(path)
        if not hangman.filename == 'exit':
            hangman.main()

    def __init__(self, path="\\"):
        self.new_file = False
        self.path = path
        self.filename = ''
        game_info = bagels.init_game(self, path, 'hng')
        if game_info:
            (self.missed_letters, self.correct_letters, self.secret_word, self.secret_key) = game_info
        return

    def __repr__(self):
        return "Hangman"

    @staticmethod
    def get_random_word(word_dict):
        # This function returns a random string from the passed dictionary of lists of strings, and the key also.
        # First, randomly select a key from the dictionary:
        word_key = random.choice(list(word_dict.keys()))
        # Second, randomly select a word from the key's list in the dictionary:
        word_index = random.randint(0, len(word_dict[word_key]) - 1)
        return [word_dict[word_key][word_index], word_key]

    def display_board(self):
        # this function displays the selected category, the hangman, the past incorrect and correct guesses, and the blanks.
        print("The secret word is in this set: " + self.secret_key)
        print(HANGMAN_PICS[len(self.missed_letters)])
        print()
        print('Missed letters:', end=' ')
        for letter in self.missed_letters:
            print(letter.upper(), end=',')
        print()
        print("Word: ", end='')
        blanks = '_' * len(self.secret_word)
        for i in range(len(self.secret_word)):  # replace blanks with correctly guessed letters
            if self.secret_word[i] in self.correct_letters:
                blanks = blanks[:i] + self.secret_word[i] + blanks[i + 1:]

        for letter in blanks:  # show the secret word with spaces in between each letter
            print(letter.upper(), end=' ')
        print()

    @staticmethod
    def get_guess(already_guessed):
        # Returns the letter the player entered. This function makes sure the player entered a single letter, and not something else.
        while True:
            print('Guess a letter, or type "quit" to exit the app.')
            guess = input().lower()
            if guess in ('quit', 'exit', 'get me outta here bruh'):
                return 'quit'
            elif len(guess) != 1:
                print('Please enter a single letter.')
            elif guess in already_guessed:
                print('You have already guessed that letter. Choose again.')
            elif guess not in 'abcdefghijklmnopqrstuvwxyz':
                print('Please enter a LETTER.')
            else:
                return guess

    def setup(self):
        self.new_file = True
        self.missed_letters = ''
        self.correct_letters = ''
        (self.secret_word, self.secret_key) = self.get_random_word(words)
        return

    def quit(self):
        if self.new_file:
            self.filename = input("File name?\n") + '.hng'
        try:
            game = open(self.path + "\\" + self.filename, 'w')
            game.write(Loading.caesar_encrypt("{}\t{}\t{}\t{}".format(self.missed_letters, self.correct_letters, self.secret_word, self.secret_key)))
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)

    def main(self):
        # This section prints the first message, resets the correct and incorrect letters, assigns secret words and keys, and sets the game to be running.
        print('H A N G M A N')
        game_is_done = False
        if self.new_file:
            self.setup()
        else:
            print('Welcome back! Your progress has been restored.')
        # This while loop continues the guessing until the guesses are up or if the word was correctly guessed.
        while True:
            self.display_board()

            # Let the player type in a letter.
            guess = self.get_guess(self.missed_letters + self.correct_letters)
            if guess == 'quit':
                self.quit()
                Loading.returning("Saving game progress...", 2)
                return
            elif guess in self.secret_word:  # This adds the correct letter to the blanks.
                self.correct_letters = self.correct_letters + guess

                # Check if the player has won
                found_all_letters = True
                for i in range(len(self.secret_word)):
                    if self.secret_word[i] not in self.correct_letters:
                        found_all_letters = False
                        break
                if found_all_letters:
                    print('Yes! The secret word is "' + self.secret_word + '"! You have won!')
                    game_is_done = True
            else:  # This just loops the player, adding their incorrect letter to the list of incorrect guesses.
                self.missed_letters = self.missed_letters + guess

                # Check if player has guessed too many times and lost
                if len(self.missed_letters) == len(HANGMAN_PICS) - 1:
                    self.display_board()
                    print('You have run out of guesses!\nAfter ' + str(len(self.missed_letters)) + ' missed guesses and ' +
                          str(len(self.correct_letters)) + ' correct guesses, the word was "' + self.secret_word + '"')
                    game_is_done = True

            # Ask the player if they want to play again (but only if the game is done).
            if game_is_done:
                os.remove(self.path + self.filename)
                if input('Do you want to play again? (yes or no)\n').lower().startswith('y'):
                    self.setup()
                    game_is_done = False
                else:
                    Loading.returning_to_apps()
                    return
