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
  |     |
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

category = "games"
version = "2.2"
entries = ('hangman', '5')


def boot(os_object=None):
    """
    Used to regulate the bootup sequence for the game
    :param os_object: Operating System object, used for the path variable.
    :return: Nothing
    """
    while True:
        hangman = Hangman(os_object.path.format(os_object.current_user.username))
        if not hangman.filename == 'exit':
            if not hangman.main() == "again":
                return
        else:
            return


class Hangman:
    """
    The main class to house everything.
    """

    def __init__(self, path="\\", game_info=""):
        self.new_file = False
        self.path = path
        self.filename = ''
        if not game_info:
            game_info = bagels.init_game(self, self.path, 'hng')
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
        return "{}(G){}(G){}".format(self.missed_letters, self.correct_letters, self.secret_word)

    def __getstate__(self):
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
                guess = Loading.pocs_input(app_object=self).lower()
                if guess in ('quit', 'exit', 'get me outta here bruh'):
                    bagels.quit_game(self)
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
