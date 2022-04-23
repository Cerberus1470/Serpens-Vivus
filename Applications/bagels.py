import time
import os
from System import Loading
import random

category = "games"


def boot(os_object):
    os_object.current_user.saved_state["Bagels Game"] = "running"
    bagels = Bagels(os_object.current_user.username)
    if not bagels.filename == 'exit':
        bagels.main()


def delete(self, extension):
    while True:
        for subdir, dirs, files in os.walk('Users\\%s' % self.username):
            count = 0
            for file in files:
                if file[len(file)-3:len(file)] == extension:
                    count += 1
                    print(str(count) + '. ' + file)
        delete_game = input("Which game would you like to delete?\n")
        try:
            os.remove("Users\\{}\\{}".format(self.username, delete_game))
        except FileNotFoundError:
            try:
                os.remove("Users\\{}\\{}".format(self.username, delete_game + extension))
                pass
            except FileNotFoundError:
                Loading.returning("That file was not found.", 1)
                pass
        if input('Delete another file? "Yes" or "No".').lower() == 'yes':
            continue
        else:
            Loading.returning("The file was successfully deleted.", 2)
            return


def init_game(self, username, extension):
    self.new_file = False
    self.username = username
    while True:
        for subdir, dirs, files in os.walk('Users\\%s' % username):
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
            return 'new'
        elif self.filename == 'delete game':
            delete(self, extension)
            continue
        else:
            try:
                game = open('Users\\%s\\%s' % (username, self.filename), 'r')
            except FileNotFoundError:
                try:
                    game = open('Users\\%s\\%s' % (username, self.filename + '.{}'.format(extension)), 'r')
                    self.filename = self.filename + '.{}'.format(extension)
                except FileNotFoundError:
                    Loading.returning("Choose a valid option.", 1)
                    continue
            Loading.returning("Loading previous game...", 2)
            bruh = list(game)
            return (Loading.caesar_decrypt(bruh[0].split('\n')[0])).split('\t')


class Bagels:

    def __init__(self, username):
        self.new_file = False
        self.username = username
        self.filename = ''
        game_info = init_game(self, username, 'bgl')
        if game_info == 'new':
            (self.prev_guesses, self.num_guesses, self.num_digits, self.secret_num, self.max_guesses) = ("", "", "", "", "")
        else:
            (self.username, prev_guesses, self.num_guesses, self.num_digits, self.max_guesses, self.secret_num) = game_info
            self.prev_guesses = prev_guesses.split(',')
        return

    def __repr__(self):
        return "< I am a bagels class named " + self.__class__.__name__ + " under the user " + self.username + ">"

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
        # Returns True if num is a string made up only of digits. Otherwise returns False.
        if not num:
            return False
        for i in num:
            if i not in '0 1 2 3 4 5 6 7 8 9'.split(' '):
                return False
        return True

    @staticmethod
    def get_clues(guess, secret_num):
        # Returns a string with the pico, fermi, bagels clues to the user.
        # Make sure the lengths match.
        if len(guess) != len(secret_num):
            return 'Enter a number with {} number of digits.'.format(len(secret_num))
        if guess == secret_num:
            return 'You got it!'

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
        prev_guesses = ''
        for j in range(len(self.prev_guesses)-1):
            prev_guesses += (self.prev_guesses[j] + ',')
        prev_guesses += self.prev_guesses[len(self.prev_guesses)-1]
        game = open('Users\\%s\\%s' % (self.username, self.filename), 'w')
        game.write(Loading.caesar_encrypt("{}\t{}\t{}\t{}\t{}\t{}".format(self.username, prev_guesses, self.num_guesses, self.num_digits, self.max_guesses, self.secret_num)))
        game.close()

    def main(self):
        print('WELCOME TO BAGELS\n')
        self.startup()
        print('I am thinking of a %s-digit number. Try to guess what it is.' % self.num_digits)
        print('Here are some clues:')
        print('When I say:    That means:')
        print('  Pico         One digit is correct but in the wrong position.')
        print('  Fermi        One digit is correct and in the right position.')
        print('  Bagels       No digit is correct.')
        print('Hint: Enter different digits. Duplicate digits will produce duplicate results!')

        while True:
            guesses = int(self.max_guesses)-int(self.num_guesses)
            print('I have thought up a number. You have %s guesses to get it.' % (guesses+1))

            while int(self.num_guesses) <= int(self.max_guesses):
                # while len(guess) != int(self.num_digits) or not self.is_only_digits(guess):
                print('Guess #%s: \nType "quit" to quit.' % self.num_guesses)
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
                elif not self.is_only_digits(guess):
                    print("Use only digits.")
                clue = self.get_clues(guess, self.secret_num)
                self.prev_guesses.append(guess)
                print(clue)
                self.num_guesses = str(int(self.num_guesses) + 1)

                if guess == self.secret_num:
                    break
                if int(self.num_guesses) > int(self.max_guesses):
                    print('You ran out of guesses. The answer was %s.' % self.secret_num)

            os.remove("Users\\{}\\{}".format(self.username, self.filename))
            print('Do you want to play again? (yes or no)')
            if input().lower().startswith('y'):
                self.setup()
                pass
            else:
                Loading.returning_to_apps()
                return
