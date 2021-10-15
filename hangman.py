# This program is a game of hangman! It will randomly select a word from 4 different categories, displays what category was chosen, and gives the player 5 incorrect guesses before the potato man is hung. Dark, I know right? The fate of a man lies in your ability to guess a word. Good luck!
# Side note: I thought we were supposed to have a working program, so I just fixed the broken code. Everything works :)
import random
POTATOPICS = ['''

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
 ___    |
        |
        |
        |
        |
        |
=========''', '''

  +-----+
  |     |
 ___    |
/   \   |
        |
        |
        |
        |
=========''', '''

  +-----+
  |     |
 ___    |
/   \   |
|o o|   |
        |
        |
        |
=========''', '''

  +-----+
  |     |
 ___    |
/   \   |
|o o|   |
\_o_/   |
        |
        |
=========''']
words={#this is the word bank
    'Colors':'red orange yellow green blue indigo violet white black brown'.split(),
    'Shapes':'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon septagon octagon'.split(),
    'Fruits':'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
    'Animals':'bat bear beaver cat cougar crab deer dog donkey duck eagle fish frog goat leech lion lizard monkey moose mouse otter owl panda python rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale wolf wombat zebra'.split()}
def getRandomWord(wordDict):
    # This function returns a random string from the passed dictionary of lists of strings, and the key also.
    # First, randomly select a key from the dictionary:
    wordKey = random.choice(list(wordDict.keys()))
    # Second, randomly select a word from the key's list in the dictionary:
    wordIndex = random.randint(0, len(wordDict[wordKey]) - 1)
    return [wordDict[wordKey][wordIndex], wordKey]

def displayBoard(POTATOPICS, missedLetters, correctLetters, secretWord): #this function displays the selected category, the potato man, the past incorrect and correct guesses, and the blanks.
    print("The secret word is in this set: " + secretKey)
    print(POTATOPICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter.upper(), end=',')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # show the secret word with spaces in between each letter
        print(letter.upper(), end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter, and not something else.
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain(): #this function isnt exactly necessary... I would just integrate it into the code since it's only called from one spot.
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# This section prints the first message, resets the correct and incorrect letters, assigns secret words and keys, and sets the game to be running.
print('H A N G P O T A T O M A N')
missedLetters = ''
correctLetters = ''
secretList = getRandomWord(words)
secretWord = secretList[0]
secretKey = secretList[1]
gameIsDone = False

# This while loop continues the guessing until the guesses are up or if the word was correctly guessed.
while True:
    displayBoard(POTATOPICS, missedLetters, correctLetters, secretWord)

    # Let the player type in a letter.
    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord: # This adds the correct letter to the blanks.
        correctLetters = correctLetters + guess

        # Check if the player has won
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Yes! The secret word is "' + secretWord + '"! You have won!')
            gameIsDone = True
    else: # This just loops the player, adding their incorrect letter to the list of incorrect guesses.
        missedLetters = missedLetters + guess

        # Check if player has guessed too many times and lost
        if len(missedLetters) == len(POTATOPICS) - 1:
            displayBoard(POTATOPICS, missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
            gameIsDone = True

    # Ask the player if they want to play again (but only if the game is done).
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretList = getRandomWord(words)
            secretWord = secretList[0]
            secretKey = secretList[1]
        else:
            break
