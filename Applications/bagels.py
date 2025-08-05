"""
Bagels. The game about a secret number.
Player gets to select conditions for a secret number and then attempt to guess the number!
"""
import os
import random
from System import Loading
from Applications.cabinet import FileEngine


category = "games"
version = "3.1.1"
entries = ('bagels', 'bagels', '3')


def boot(os_object=None):
    """
    Used to regulate the bootup sequence for the game
    :param os_object: Operating System object, used for the path variable.
    :return: Nothing
    """
    while True:
        bagels = Bagels(path=os_object.path.format(os_object.current_user.username))
        if not bagels.filename == 'exit':
            if not bagels.main() == "again":
                return
        else:
            return


class Bagels:
    """
    Bagels Game. Adapted from BYU CS Part 1 and made to work with Cerberus.
    """

    def __init__(self, path="\\", game_info=""):
        self.new_file = False
        self.path = path
        self.filename = ''
        if not game_info:
            game_info = FileEngine.init(self, self.path, 'bgl')
        if self.new_file:
            while True:
                try:
                    self.new_file = True
                    self.prev_guesses = []
                    self.num_guesses = 1
                    self.num_digits = int(input('Enter the number of digits in the secret number:'))
                    self.max_guesses = int(input('Enter the number of guesses you would like to try:'))
                    base_number = int(input('Enter a base number system from 5 to 10 to use.\n'
                                            'The base number decides what range of digits to choose the secret number from.'))
                    self.secret_num = self.get_secret_num(self.num_digits, base_number)
                    break
                except (TypeError, ValueError):
                    Loading.returning("That is not a valid value.", 2)
        elif game_info:
            (prev_guesses, self.num_guesses, self.num_digits, self.max_guesses, self.secret_num) = game_info
            self.prev_guesses = prev_guesses.split(',')
            self.new_file = True if self.filename == '' else False
        return

    def __repr__(self):
        return "{}(G){}(G){}(G){}(G){}".format(','.join(self.prev_guesses), self.num_guesses, self.num_digits, self.max_guesses, self.secret_num)

    def __getstate__(self):
        return "Bagels(SS1){}(SS2){}(SS2){}(SS2){}(SS2){}".format(','.join(self.prev_guesses), self.num_guesses, self.num_digits, self.max_guesses, self.secret_num)

    def main(self):
        """
        Main loop method for the game.
        :return: Returns "again" if the user wants to play again.
        """
        print('WELCOME TO BAGELS\n')
        if not self.new_file:
            Loading.returning("Welcome Back! Your progress has been restored.", 2)
        print('I am thinking of a %s-digit number with digits ranging from 0-%s. Try to guess what it is.' % (self.num_digits, max(self.secret_num)))
        print('Here are some clues:')
        print('When I say:    That means:')
        print('  Fermi        One digit is correct and in the right position.')
        print('  Pico         One digit is correct but in the wrong position.')
        print('  Bagels       No digit is correct.')
        print('Hint: Enter different digits. Duplicate digits will produce duplicate results!')

        while True:
            print('I have thought up a number. You have %s guesses to get it.' % (int(self.max_guesses) - int(self.num_guesses) + 1))

            while int(self.num_guesses) <= int(self.max_guesses):
                if not self.prev_guesses or not self.prev_guesses[0] == '':
                    for i in self.prev_guesses:
                        print("Guess: {}, Clue: {}".format(i, self.get_clues(i)))
                print('Guess #%s: \nType "help" for help. Type "quit" to quit.' % self.num_guesses)
                guess = Loading.pocs_input(app_object=self)
                if guess == 'quit':
                    FileEngine.quit(self, ".bgl")
                    return
                elif guess == 'help':
                    print('Here are some clues:')
                    print('When I say:    That means:')
                    print('  Fermi        One digit is correct and in the right position.')
                    print('  Pico         One digit is correct but in the wrong position.')
                    print('  Bagels       No digit is correct.')
                clue = self.get_clues(guess)
                if clue:
                    self.prev_guesses.append(guess)
                    print(clue)
                    self.num_guesses = str(int(self.num_guesses) + 1)

                if guess == self.secret_num:
                    break
                if int(self.num_guesses) > int(self.max_guesses):
                    print('You ran out of guesses. The answer was %s.' % self.secret_num)
            if not self.new_file:
                os.remove(self.path + '\\' + self.filename)
            if Loading.pocs_input('Do you want to play again? (yes or no)\n').lower().startswith('y'):
                return "again"
            else:
                Loading.returning_to_apps()
                return

    @staticmethod
    def get_secret_num(num_digits, base_number):
        """
        Method to obtain the secret number
        :param num_digits: How many digits in the secret number
        :param base_number: Base system for the secret number
        :return: The new secret number
        """
        # Returns a string that is num_digits long, made up of unique random digits.
        numbers = list(range(num_digits))
        for i in range(num_digits):
            numbers[i] = random.randint(0, base_number)
        random.shuffle(numbers)
        secret_num = ''
        for i in range(num_digits):
            secret_num += str(numbers[i])
        return str(secret_num)

    def get_clues(self, guess):
        """
        Method to obtain clues from the guessed number
        :param guess: The guessed number
        :return: Return the clues!
        """
        # Returns a string with the pico, fermi, bagels clues to the user.
        # Make sure the lengths match.
        if len(guess) != len(self.secret_num):
            print('Enter a number with {} digits.'.format(len(self.secret_num)))
            return
        clue = []
        if guess:
            if not all([i in '0123456789' for i in guess]):
                print("Use only digits.")
                return
            if guess == self.secret_num:
                print("You got it!")
                return 1
            for i in range(len(guess)):
                if guess[i] == self.secret_num[i]:
                    clue.append('Fermi')
                elif guess[i] in self.secret_num:
                    clue.append('Pico')
            if len(clue) == 0:
                return 'Bagels'

        clue.sort()
        return ' '.join(clue)
