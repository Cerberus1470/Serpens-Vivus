# This is a guess the number game.
import random
import time

guessesTaken = 0

print('Hello! Input a range of numbers.')
print('lower limit')
a = input()
aint = int(a)
print('upper limit')
b = input()
bint = int(b)

number = random.randint(aint, bint)
print('Well, I am thinking of a number between '+a+' and '+b+'.')
print('How many guesses would you like?')
guessesGiven = input()
guessesGiven = int(guessesGiven)

while guessesTaken < guessesGiven:
    print('Take a guess.') # There are four spaces in front of print.
    guess = input()
    guess = int(guess)

    guessesTaken = guessesTaken + 1

    if guess < number:
        print('Your guess is too low.') # There are eight spaces in front of print.

    if guess > number:
        print('Your guess is too high.')

    if guess == number:
        break

if guess == number:
    guessesTaken = str(guessesTaken)
    print('Good job! You guessed my number in ' + guessesTaken + ' guesses!')

if guess != number:
    number = str(number)
    print('Nope. The number I was thinking of was ' + number)

time.sleep(10)
