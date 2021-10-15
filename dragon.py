import random
import time

def createName():
    print('What is your name?')
    name = input()
    print('Very well, ' + name + ' good luck on your journey.')
    return name

def displayIntro():
    print(playerName+' is/are in a land full of dragons. In front of '+playerName+',')
    print(playerName+' see(s) two caves. In one cave, the dragon is friendly')
    print('and will share his treasure with you. The other dragon')
    print('is greedy and hungry, and will eat '+playerName+' on sight.')
    print()

def chooseCave():
    cave = ''
    while cave != '1' and cave != '2' and cave != '3':
        print('Which cave will you go into? (1, 2, or 3)')
        cave = input()

    return cave

def checkCave(chosenCave):
    print('You approach the cave...')
    time.sleep(2)
    print('It is dark and spooky...')
    time.sleep(2)
    print('A large dragon jumps out in front of you! He opens his jaws and...')
    print()
    time.sleep(2)

    friendlyCave = random.randint(1, 3)

    if chosenCave == str(friendlyCave):
        print('Gives you his treasure!')
    elif chosenCave >= str(friendlyCave):
        print('Lets you look at the treasure and then eats you!')
    else:
        print('Gobbles you down in one bite!')

playAgain = 'yes'
while playAgain == 'yes' or playAgain == 'y':

    playerName = createName()

    displayIntro()

    caveNumber = chooseCave()

    checkCave(caveNumber)

    print('Do you want to play again? (yes or no)')
    playAgain = input()
