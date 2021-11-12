import random
import time


class Bagels:

    def __init__(self):
        return

    def __repr__(self):
        return "< I am a bagels class named " + self.__class__.__name__ + ">"

    def get_secret_num(self, num_digits, base_number):
        # Returns a string that is num_digits long, made up of unique random digits.
        numbers = list(range(base_number))
        random.shuffle(numbers)
        secret_num = ''
        for i in range(num_digits):
            secret_num += str(numbers[i])
        return secret_num

    def is_only_digits(self, num):
        # The map() method in the line of code below converts a list of values to a string and returns that string.
        # base_String_Elements = ''.join(map(str, list(range(baseNumber))))
        # for i in num:
        #   if i not in base_String_Elements:
        #        return False
        # Returns True if num is a string made up only of digits. Otherwise returns False.
        if num == '':
            return False

        for i in num:
            if i not in '0 1 2 3 4 5 6 7 8 9'.split():
                return False

        return True

    def get_clues(self, guess, secret_num):
        # Returns a string with the pico, fermi, bagels clues to the user.
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

    def play_again(self):
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')

    def setup(self, stats):
        last_guess = ''
        num_guesses = 1
        num_digits = int(input('Enter the number of digits in the secret number:'))
        max_guesses = int(input('Enter the number of guesses you would like to try:'))
        basenumber = int(input('Enter a base number system from 5 to 10 to use.\n'
                               'The base number decides what range of digits to choose the secret number from.'))
        secret_num = self.get_secret_num(num_digits, basenumber)
        return last_guess, num_guesses, num_digits, max_guesses, secret_num

    def main(self, stats, prog):
        stats["Bagels Game"] = "running"
        print('WELCOME TO BAGELS')
        print(' ')
        last_guess = prog[0]
        num_guesses = prog[1]
        num_digits = prog[2]
        secret_num = prog[3]
        max_guesses = prog[4]
        if last_guess == ' ' or num_guesses == ' ' or num_digits == ' ' or secret_num == ' ' or max_guesses == ' ':
            last_guess, num_guesses, num_digits, max_guesses, secret_num = self.setup(stats)

        print('I am thinking of a %s-digit number. Try to guess what it is.' % num_digits)
        print('Here are some clues:')
        print('When I say:    That means:')
        print('  Pico         One digit is correct but in the wrong position.')
        print('  Fermi        One digit is correct and in the right position.')
        print('  Bagels       No digit is correct.')
        print('Hint: Enter different digits. Duplicate digits will produce duplicate results!')

        while True:
            guesses = int(max_guesses)-int(num_guesses)
            print('I have thought up a number. You have %s guesses to get it.' % (guesses+1))

            while int(num_guesses) <= int(max_guesses):
                guess = ''
                while len(guess) != int(num_digits) or not self.is_only_digits(guess):
                    print('Guess #%s: \nType "quit" to quit.' % num_guesses)
                    guess = input()
                    if guess == 'quit':
                        print("Saving game progress...")
                        time.sleep(3)
                        return last_guess, num_guesses, num_digits, secret_num, max_guesses
                last_guess = guess
                clue = self.get_clues(last_guess, secret_num)
                print(clue)
                num_guesses += 1

                if guess == secret_num:
                    break
                if num_guesses > max_guesses:
                    print('You ran out of guesses. The answer was %s.' % secret_num)

            if self.play_again():
                self.setup(stats)
                pass
            else:
                return ' ', ' ', ' ', ' ', ' '
