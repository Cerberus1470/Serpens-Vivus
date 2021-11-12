# This program is a game of hangman! It will randomly select a word from 4 different categories, displays what category was chosen, and gives the player 5 incorrect guesses before the potato man is hung. Dark, I know right? The fate of a man lies in
# your ability to guess a word. Good luck! Side note: I thought we were supposed to have a working program, so I just fixed the broken code. Everything works :)
import random
import time

HANGMANPICS = ['''

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
    def get_random_word(self, word_dict):
        # This function returns a random string from the passed dictionary of lists of strings, and the key also.
        # First, randomly select a key from the dictionary:
        word_key = random.choice(list(word_dict.keys()))
        # Second, randomly select a word from the key's list in the dictionary:
        word_index = random.randint(0, len(word_dict[word_key]) - 1)
        return [word_dict[word_key][word_index], word_key]

    def display_board(self, hangman_pics, missed_letters, correct_letters, secret_word, secret_key):
        # this function displays the selected category, the potato man, the past incorrect and correct guesses, and the blanks.
        print("The secret word is in this set: " + secret_key)
        print(hangman_pics[len(missed_letters)])
        print()
        print('Missed letters:', end=' ')
        for letter in missed_letters:
            print(letter.upper(), end=',')
        print()
        print("Word: ", end='')

        blanks = '_' * len(secret_word)

        for i in range(len(secret_word)):  # replace blanks with correctly guessed letters
            if secret_word[i] in correct_letters:
                blanks = blanks[:i] + secret_word[i] + blanks[i + 1:]

        for letter in blanks:  # show the secret word with spaces in between each letter
            print(letter.upper(), end=' ')
        print()

    def get_guess(self, already_guessed):
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
        missed_letters = ''
        correct_letters = ''
        (secret_word, secret_key) = self.get_random_word(words)
        return missed_letters, correct_letters, secret_word, secret_key

    def main(self, stats, prog):
        stats["Hangman"] = 'running'
        # This section prints the first message, resets the correct and incorrect letters, assigns secret words and keys, and sets the game to be running.
        print('H A N G M A N')
        missed_letters = prog[0]
        correct_letters = prog[1]
        secret_word = prog[2]
        secret_key = prog[3]
        if (missed_letters == '' and correct_letters == '') or secret_word == ' ' or secret_key == ' ':
            (missed_letters, correct_letters, secret_word, secret_key) = self.setup()
        else:
            print("Welcome back!")
        game_is_done = False

        # This while loop continues the guessing until the guesses are up or if the word was correctly guessed.
        while True:
            self.display_board(HANGMANPICS, missed_letters, correct_letters, secret_word, secret_key)

            # Let the player type in a letter.
            guess = self.get_guess(missed_letters + correct_letters)
            if guess == 'quit':
                return missed_letters, correct_letters, secret_word, secret_key
            elif guess in secret_word:  # This adds the correct letter to the blanks.
                correct_letters = correct_letters + guess

                # Check if the player has won
                found_all_letters = True
                for i in range(len(secret_word)):
                    if secret_word[i] not in correct_letters:
                        found_all_letters = False
                        break
                if found_all_letters:
                    print('Yes! The secret word is "' + secret_word + '"! You have won!')
                    game_is_done = True
            else:  # This just loops the player, adding their incorrect letter to the list of incorrect guesses.
                missed_letters = missed_letters + guess

                # Check if player has guessed too many times and lost
                if len(missed_letters) == len(HANGMANPICS) - 1:
                    self.display_board(HANGMANPICS, missed_letters, correct_letters, secret_word, secret_key)
                    print('You have run out of guesses!\nAfter ' + str(len(missed_letters)) + ' missed guesses and ' + str(len(correct_letters)) + ' correct guesses, the word was "' + secret_word + '"')
                    game_is_done = True

            # Ask the player if they want to play again (but only if the game is done).
            if game_is_done:
                print('Do you want to play again? (yes or no)')
                if input().lower().startswith('y'):
                    missed_letters = ''
                    correct_letters = ''
                    game_is_done = False
                    (secret_word, secret_key) = self.get_random_word(words)
                else:
                    print("Returning to the login screen in 3 seconds.")
                    time.sleep(3)
                    return ' ', ' ', ' ', ' '
