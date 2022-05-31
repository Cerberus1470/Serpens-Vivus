import time
import os
from System import Loading
import random


def delete(path, extension):
    while True:
        for subdir, dirs, files in os.walk(path):
            count = 0
            for file in files:
                if file[len(file)-3:len(file)] == extension:
                    count += 1
                    print(str(count) + '. ' + file)
        delete_game = input("Which game would you like to delete?\n")
        try:
            os.remove("{}\\{}".format(path, delete_game))
        except FileNotFoundError:
            try:
                os.remove("{}\\{}".format(path, '{}.{}'.format(delete_game, extension)))
                pass
            except FileNotFoundError:
                Loading.returning("That file was not found.", 1)
                pass
        Loading.returning("The file was successfully deleted.", 2)
        if input('Delete another file? "Yes" or "No".').lower() == 'yes':
            continue
        else:
            Loading.returning("Returning to the game...", 2)
            return


def init_game(self, path, extension):
    while True:
        for subdir, dirs, files in os.walk(path):
            count = 0
            for file in files:
                if file[len(file)-3:len(file)] == extension:
                    count += 1
                    print(str(count) + '. ' + file)
            print(str(count+1) + '. New Game')
            print(str(count+2) + '. Delete Game')
        self.filename = input('Which file would you like to open? Type "exit" to exit.\n').lower()
        if self.filename == 'exit':
            self.filename = "exit"
            Loading.returning_to_apps()
            return
        if self.filename == 'new game':
            self.new_file = True
            return
        elif self.filename == 'delete game':
            delete(path, extension)
            continue
        else:
            try:
                if self.filename[len(self.filename)-3:len(self.filename)] == extension:
                    game = open("{}\\{}".format(path, self.filename), 'r')
                else:
                    game = open("{}\\{}".format(path, '{}.{}'.format(self.filename, extension)), 'r')
                    self.filename = '{}.{}'.format(self.filename, extension)
            except FileNotFoundError:
                Loading.returning("Choose a valid option.", 1)
                continue
            Loading.returning("Loading previous game...", 2)
            bruh = list(game)
            if extension == "snr":
                return bruh
            return (Loading.caesar_decrypt(bruh[0].split('\n')[0])).split('\t')


class Bagels:
    category = "games"

    @staticmethod
    def boot(path="\\"):
        bagels = Bagels(path)
        if not bagels.filename == 'exit':
            bagels.main()

    def __init__(self, path="\\"):
        self.new_file = False
        self.path = path
        self.filename = ''
        game_info = init_game(self, path, 'bgl')
        if self.new_file:
            (self.prev_guesses, self.num_guesses, self.num_digits, self.secret_num, self.max_guesses) = ("", -1, "", "", -1)
        elif game_info:
            (prev_guesses, self.num_guesses, self.num_digits, self.max_guesses, self.secret_num) = game_info
            self.prev_guesses = prev_guesses.split(',')
        return

    def __repr__(self):
        return "< I am a bagels class named " + self.__class__.__name__ + ">"

    @staticmethod
    def get_secret_num(num_digits, base_number):
        # Returns a string that is num_digits long, made up of unique random digits.
        numbers = list(range(num_digits))
        for i in range(num_digits):
            numbers[i] = random.randint(0, base_number)
        random.shuffle(numbers)
        secret_num = ''
        for i in range(num_digits):
            secret_num += str(numbers[i])
        return str(secret_num)

    @staticmethod
    def is_only_digits(num):
        # Returns True if num is a string made up only of digits. Otherwise, returns False.
        if not num:
            return False
        for i in num:
            if i not in '0 1 2 3 4 5 6 7 8 9'.split(' '):
                return False
        return True

    def get_clues(self, guess, secret_num):
        # Returns a string with the pico, fermi, bagels clues to the user.
        # Make sure the lengths match.
        if len(guess) != len(secret_num):
            print('Enter a number with {} digits.'.format(len(secret_num)))
            return
        if not self.is_only_digits(guess):
            print("Use only digits.")
            return
        if guess == secret_num:
            print("You got it!")
            return

        clue = []
        for i in range(len(guess)):
            if guess[i] == secret_num[i]:
                clue.append('Fermi')
            elif guess[i] in secret_num:
                clue.append('Pico')
        if len(clue) == 0:
            return 'Bagels'

        clue.sort()
        return ' '.join(clue)

    def setup(self):
        self.new_file = True
        self.prev_guesses = []
        self.num_guesses = 1
        self.num_digits = int(input('Enter the number of digits in the secret number:'))
        self.max_guesses = int(input('Enter the number of guesses you would like to try:'))
        basenumber = int(input('Enter a base number system from 5 to 10 to use.\n'
                               'The base number decides what range of digits to choose the secret number from.'))
        self.secret_num = self.get_secret_num(self.num_digits, basenumber)
        return

    def startup(self):
        if self.num_guesses == '' or self.num_digits == '' or self.secret_num == '' or self.max_guesses == '':
            self.setup()
        else:
            print("Welcome Back! Your progress has been restored.")
            Loading.returning("There are {} digits in the secret number, and you have {} guesses left.".format(self.num_digits, str(int(self.max_guesses) - int(self.num_guesses) + 1)), 3)
            print("Here is a list of your previous guesses.")
            for i in self.prev_guesses:
                print("Guess: {}, Clue: {}".format(i, self.get_clues(i, self.secret_num)))
            time.sleep(3)

    def quit(self):
        if self.new_file:
            self.filename = input("File name?\n") + '.bgl'
        prev_guesses = ','.join(self.prev_guesses)
        game = open(self.path + "\\" + self.filename, 'w')
        game.write(Loading.caesar_encrypt("{}\t{}\t{}\t{}\t{}".format(prev_guesses, self.num_guesses, self.num_digits, self.max_guesses, self.secret_num)))
        game.close()

    def main(self):
        print('WELCOME TO BAGELS\n')
        self.startup()
        print('I am thinking of a %s-digit number. Try to guess what it is.' % self.num_digits)
        print('Here are some clues:')
        print('When I say:    That means:')
        print('  Fermi        One digit is correct and in the right position.')
        print('  Pico         One digit is correct but in the wrong position.')
        print('  Bagels       No digit is correct.')
        print('Hint: Enter different digits. Duplicate digits will produce duplicate results!')

        while True:
            guesses = int(self.max_guesses)-int(self.num_guesses)
            print('I have thought up a number. You have %s guesses to get it.' % (guesses+1))

            while int(self.num_guesses) <= int(self.max_guesses):
                # while len(guess) != int(self.num_digits) or not self.is_only_digits(guess):
                print('Guess #%s: \nType "help" for help. Type "quit" to quit.' % self.num_guesses)
                guess = input()
                if guess == 'quit':
                    self.quit()
                    Loading.returning("Saving game progress...", 2)
                    return
                elif guess == 'help':
                    print('Here are some clues:')
                    print('When I say:    That means:')
                    print('  Pico         One digit is correct but in the wrong position.')
                    print('  Fermi        One digit is correct and in the right position.')
                    print('  Bagels       No digit is correct.')
                clue = self.get_clues(guess, self.secret_num)
                self.prev_guesses.append(guess)
                print(clue)
                self.num_guesses = str(int(self.num_guesses) + 1)

                if guess == self.secret_num:
                    break
                if int(self.num_guesses) > int(self.max_guesses):
                    print('You ran out of guesses. The answer was %s.' % self.secret_num)
            if not self.new_file:
                os.remove(self.path + self.filename)
            if input('Do you want to play again? (yes or no)\n').lower().startswith('y'):
                self.setup()
                pass
            else:
                Loading.returning_to_apps()
                return
