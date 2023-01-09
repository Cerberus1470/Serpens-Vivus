"""
This program is a game of hangman! It will randomly select a word from 4 different categories, displays what category was chosen, and gives the player 5 incorrect guesses before the potato man is hung. Dark, I know right? The fate of a man lies in
your ability to guess a word. Good luck! Side note: I thought we were supposed to have a working program, so I just fixed the broken code. Everything works :)
"""
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
    """
    The main class to house everything.
    """
    category = "games"

    @staticmethod
    def boot(path="\\"):
        """
        Used to regulate the bootup sequence for the game
        :param path: Path to pass on to everything
        :return: Nothing
        """
        while True:
            hangman = Hangman(path)
            if not hangman.filename == 'exit':
                if not hangman.main() == "again":
                    return
            else:
                return

    def __init__(self, path="\\", game_info=""):
        self.new_file = False
        self.path = path
        self.filename = ''
        if not game_info:
            game_info = bagels.init_game(self, path, 'hng')
        if self.new_file:
            self.new_file = True
            self.missed_letters = ''
            self.correct_letters = ''
            self.secret_word = random.choice(random.choice(list(words.values())))
        elif game_info:
            (self.missed_letters, self.correct_letters, self.secret_word) = game_info
            self.new_file = True if self.filename == '' else False
        return

    def __repr__(self):
        return "Hangman(SS1){}(SS2){}(SS2){}".format(self.missed_letters, self.correct_letters, self.secret_word)

    def main(self):
        """
        Main loop method for the game.
        :return: Nothing.
        """
        # This section prints the first message, resets the correct and incorrect letters, assigns secret words and keys, and sets the game to be running.
        print('H A N G M A N')
        game_is_done = False
        # if self.new_file:
        #     self.setup()
        if not self.new_file:
            print('Welcome back! Your progress has been restored.')
        # This while loop continues the guessing until the guesses are up or if the word was correctly guessed.
        while True:
            print("The secret word is in this set: " + [i for i in words.keys() if self.secret_word in words[i]][0])
            print(HANGMAN_PICS[len(self.missed_letters)])
            print('\nMissed letters: {}'.format(','.join(i.upper() for i in self.missed_letters)))
            print(' '.join([i if i in self.correct_letters else '_' for i in self.secret_word]))
            # Let the player type in a letter.
            while True:
                print('Guess a letter, or type "quit" to exit the app.')
                guess = Loading.pocs_input("", self).lower()
                if guess in ('quit', 'exit', 'get me outta here bruh'):
                    self.quit()
                    Loading.returning("Saving game progress...", 2)
                    return
                elif len(guess) != 1:
                    print('Please enter a single letter.')
                elif guess in (self.correct_letters + self.missed_letters):
                    print('You have already guessed that letter. Choose again.')
                elif guess not in 'abcdefghijklmnopqrstuvwxyz':
                    print('Please enter a LETTER.')
                else:
                    break
            if guess in self.secret_word:  # This adds the correct letter to the blanks.
                self.correct_letters += guess

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
                self.missed_letters += guess

                # Check if player has guessed too many times and lost
                if len(self.missed_letters) == len(HANGMAN_PICS) - 1:
                    print("The secret word is in this set: " + [i for i in words.keys() if self.secret_word in words[i]][0])
                    print(HANGMAN_PICS[len(self.missed_letters)])
                    print('\nMissed letters: {}'.format(','.join(i.upper() for i in self.missed_letters)))
                    print(' '.join([i if i in self.correct_letters else '_' for i in self.secret_word]))
                    print('You have run out of guesses!\nAfter ' + str(len(self.missed_letters)) + ' missed guesses and ' +
                          str(len(self.correct_letters)) + ' correct guesses, the word was "' + self.secret_word + '"')
                    game_is_done = True

            # Ask the player if they want to play again (but only if the game is done).
            if game_is_done:
                if not self.new_file:
                    os.remove(self.path + self.filename)
                if Loading.pocs_input('Do you want to play again? (yes or no)\n', self).lower().startswith('y'):
                    return "again"
                else:
                    Loading.returning_to_apps()
                    return

    def quit(self):
        """
        Method to regulate quitting and saving progress
        :return: Nothing.
        """
        if self.new_file:
            self.filename = input("File name?\n") + '.hng'
        try:
            game = open(self.path + "\\" + self.filename, 'w')
            game.write(Loading.caesar_encrypt("{}(G){}(G){}".format(self.missed_letters, self.correct_letters, self.secret_word)))
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)

    @staticmethod
    @DeprecationWarning
    def get_random_word(word_dict):
        """
        Method to get a random word
        :param word_dict: Words to limit selection to
        :return: Random word
        """
        # This function returns a random string from the passed dictionary of lists of strings, and the key also.
        # First, randomly select a key from the dictionary:
        word_key = random.choice(list(word_dict.keys()))
        # Second, randomly select a word from the key's list in the dictionary:
        word_index = random.randint(0, len(word_dict[word_key]) - 1)
        return [word_dict[word_key][word_index], word_key]

    @DeprecationWarning
    def display_board(self):
        """
        Method to display the Hangman Board, the selected category, the hangman, the past incorrect and correct guesses, and the blanks.
        :return: Nothing
        """
        # this function displays the selected category, the hangman, the past incorrect and correct guesses, and the blanks.
        print("The secret word is in this set: " + [i for i in words.keys() if self.secret_word in words[i]][0])
        print(HANGMAN_PICS[len(self.missed_letters)])
        print()
        print('Missed letters: {}'.format(','.join(i.upper() for i in self.missed_letters)))
        # for letter in self.missed_letters:
        #     print(letter.upper(), end=',')
        print("Word: ", end='')
        blanks = '_' * len(self.secret_word)
        for i in range(len(self.secret_word)):  # replace blanks with correctly guessed letters
            if self.secret_word[i] in self.correct_letters:
                blanks = blanks[:i] + self.secret_word[i] + blanks[i + 1:]

        for letter in blanks:  # show the secret word with spaces in between each letter
            print(letter.upper(), end=' ')
        print()
        return

    @staticmethod
    @DeprecationWarning
    def get_guess(already_guessed):
        """
        Method to get a guess from the player
        :param already_guessed: Characters already guessed
        :return: The player's guess
        """
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

    @DeprecationWarning
    def setup(self):
        """
        Method to set everything up.
        :return: Nothing.
        """
        self.new_file = True
        self.missed_letters = ''
        self.correct_letters = ''
        # self.secret_word = self.get_random_word(words)
        return
