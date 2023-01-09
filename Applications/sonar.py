"""
Sonar Treasure Hunt
"""

import random
import math
import os
from System import Loading
from Applications import bagels


class Sonar:
    """
    The class that contains all.
    """
    category = 'games'

    @staticmethod
    def boot(path="\\"):
        """
        Used to regulate the bootup sequence for the game
        :param path: Path to pass on to everything
        :return: Nothing
        """
        while True:
            sonar = Sonar(path)
            if not sonar.filename == 'exit':
                if not sonar.main() == "again":
                    return
            else:
                return

    def __init__(self, path="\\", game_info=""):
        self.new_file = False
        self.filename = ''
        self.path = path
        if not game_info:
            game_info = bagels.init_game(self, path, 'snr')
        self.board = [['-' if random.randint(0, 1) == 0 else '~' for _ in range(40)] for _ in range(10)]
        if self.new_file:
            self.new_file = True
            print('Would you like to view the instructions? (yes/no)')
            if input().lower().startswith('y'):
                self.show_instructions()
            print('How many sonar devices would you like?')
            self.devices = int(input())
            print('How many treasure chests should there be?')
            chests = int(input())
            self.chests = self.get_random_chests(chests)
            self.previous_moves = []
        elif game_info:
            (devices, chests, previous_moves) = game_info
            self.devices = int(devices)
            # self.board = Loading.caesar_decrypt(board[0:len(board) - 1]).split('\t')
            # for i in range(len(self.board)):
            #     self.board[i] = self.board[i].split(',')
            self.chests = [[int(j), int(k)] for j, k in [i.split(',') for i in chests.split('(C)')]]
            self.previous_moves = previous_moves.split('(P)')
            if self.previous_moves == [""]:
                self.previous_moves = []
            self.previous_moves = [[int(j), int(k)] for j, k in [i.split(',') for i in self.previous_moves]]
            self.new_file = True if self.filename == '' else False
            self.board = [['-' if random.randint(0, 1) == 0 else '~' for _ in range(40)] for _ in range(10)]
            for x, y in self.previous_moves:
                self.make_move(x, y)
        return

    def __repr__(self):
        return "Sonar(SS1){}(SS2){}(SS2){}".format(str(self.devices), '(C)'.join([(','.join(str(j) for j in i)) for i in self.chests]),
                                                   '(P)'.join([(','.join(str(j) for j in i)) for i in self.previous_moves]))

    def main(self):
        """
        Main method for all gameplay.
        :return: Nothing.
        """
        print('S O N A R !\n')
        if not self.new_file:
            print("Welcome back!")
        while True:
            self.draw_board()
            while self.devices > 0:
                # Show sonar device and chest statuses.
                print('You have {} sonar device(s) left. {} treasure chest(s) remaining.'.format(self.devices, len(self.chests)))
                print('Where do you want to drop the next sonar device? (0-9 0-39) (or type quit)')
                while True:
                    move = Loading.pocs_input("", self)
                    if move.lower() == 'quit':
                        self.quit()
                        return
                    move = move.split()
                    if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and 0 <= int(move[0]) <= 9 and 0 <= int(move[1]) <= 39:
                        if [int(move[0]), int(move[1])] in self.previous_moves:
                            print('There is already a sonar device placed there.')
                        else:
                            x, y = [int(move[0]), int(move[1])]
                            break
                    else:
                        print('Enter a number from 0 to 9, a space, then a number from 0 to 39.')
                # x, y = self.enter_player_move()
                # if x == 'quit' and y == 'quit':
                #     return
                # We must track all moves so that sonar devices can be updated.
                self.previous_moves.append([x, y])

                moveResult = self.make_move(x, y)
                if moveResult == 'You have found a sunken treasure chest!':
                    # Update all the sonar devices currently on the map.
                    for x, y in self.previous_moves:
                        self.make_move(x, y)
                self.draw_board()
                print(moveResult)

                if len(self.chests) == 0:
                    print('You have found all the sunken treasure chests! Congratulations and good game!')
                    break

                self.devices -= 1

            if self.devices == 0:
                print("We've run out of sonar devices! Now we have to turn the ship around and head\nfor home with treasure chests still out there! Game over.")
                print(' The remaining chests were here:')
                for x, y in self.chests:
                    print(' {}, {}'.format(x, y))
            if not self.new_file:
                os.remove(self.path + '\\' + self.filename)
            if Loading.pocs_input('Do you want to play again? (yes or no)', self).lower().startswith('y'):
                return "again"
            else:
                Loading.returning_to_apps()
                return

    @staticmethod
    @DeprecationWarning
    def get_new_board():
        """
        Method to get a new board.
        :return:
        """
        # Create a new 10x40 board data structure.
        board = []
        # The main list is a list of 10 lists.
        for x in range(10):
            board.append([])
            # Each list in the main list has 40 single-character strings.
            for y in range(40):
                # Use different characters for the ocean to make it more readable.
                if random.randint(0, 1) == 0:
                    board[x].append('~')
                else:
                    board[x].append('-')
        return board

    def draw_board(self):
        """
        Method to display the board.
        :return: Nothing.
        """
        # Draw the board data structure.
        tensDigitsLine = '   '
        # Initial space for the numbers down the left side of the board
        for i in range(1, 4):
            tensDigitsLine += (' ' * 9) + str(i)

        # Print the numbers across the top of the board.
        print(tensDigitsLine)
        print('  ' + ('0123456789' * 4))

        # Print each of the 10 rows.
        for row in range(10):
            # Create the string for this row on the board.
            boardRow = ''
            for column in range(40):
                boardRow += self.board[row][column]

            print('{} {} {}'.format(row, boardRow, row))

        # Print the numbers across the bottom of the board.
        print('  ' + ('0123456789' * 4))
        print(tensDigitsLine)

    @staticmethod
    def get_random_chests(num_chests):
        """
        Method to generate chests
        :param num_chests: Number of chests to generate.
        :return: The list of generated chests.
        """
        # Create a list of chest data structures (two-item lists of x, y int coordinates).
        chests = []
        while len(chests) < num_chests:
            newChest = [random.randint(0, 9), random.randint(0, 39)]
            # Make sure a chest is not already here.
            if newChest not in chests:
                chests.append(newChest)
        return chests

    @staticmethod
    @DeprecationWarning
    def is_on_board(x, y):
        """
        Method to verify if the move is on the board
        :param x: X-coordinate
        :param y: Y-coordinate
        :return: True if position is on the board, False if not.
        """
        # Return True if the coordinates are on the board; otherwise, return False.
        return

    def make_move(self, x, y):
        """
        Method to make move on the board
        :param x: X-coordinate
        :param y: Y-coordinate
        :return: A clue!
        """
        # Change the board data structure with a sonar device character. Remove treasure chests from the chests list as they are found.
        # Return False if this is an invalid move.
        # Otherwise, return the string of the result of this move.
        # Any chest will be closer than 100.
        smallestDistance = 100
        for cx, cy in self.chests:
            distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))
            # We want the closest treasure chest.
            if distance < smallestDistance:
                smallestDistance = distance

        smallestDistance = round(smallestDistance)

        if smallestDistance == 0:
            # xy is directly on a treasure chest!
            self.chests.remove([x, y])
            return 'You have found a sunken treasure chest!'
        else:
            if smallestDistance < 10:
                self.board[x][y] = str(smallestDistance)
                return 'Treasure detected at a distance of {} from the sonar device.'.format(smallestDistance)
            else:
                self.board[x][y] = 'X'
                return 'Sonar did not detect anything. All treasure chests out of range.'

    @DeprecationWarning
    def enter_player_move(self):
        """
        Method to ask for a player move. Filters literally every incorrect input.
        :return: The move, if valid.
        """
        # Let the player enter their move. Return a two-item list of int xy coordinates.
        print('Where do you want to drop the next sonar device? (0-9 0-39) (or type quit)')
        while True:
            move = input()
            if move.lower() == 'quit':
                self.quit()
                return ['quit', 'quit']

            move = move.split()
            if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and 0 <= int(move[0]) <= 9 and 0 <= int(move[1]) <= 39:
                if [int(move[0]), int(move[1])] in self.previous_moves:
                    print('You already moved there.')
                    continue
                return [int(move[0]), int(move[1])]

            print('Enter a number from 0 to 9, a space, then a number from 0 to 39.')

    @staticmethod
    def show_instructions():
        """
        Method to show instructions on prompt.
        :return: Nothing.
        """
        input('''Instructions:
                You are the captain of the Simon, a treasure-hunting ship. Your current mission
                is to use sonar devices to find three sunken treasure chests at the bottom of
                the ocean. But you only have cheap sonar that finds distance, not direction.
                
                Enter the coordinates to drop a sonar device. The ocean map will be marked with
                how far away the nearest chest is, or an X if it is beyond the sonar device's
                range. For example, the C marks are where chests are. The sonar device shows a
                3 because the closest chest is 3 spaces away.
                
                1 2 3
                012345678901234567890123456789012
                
                0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
                1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
                2 `~`C``3`~~~~`C`~~~~`````~~``~~~`` 2
                3 ````````~~~`````~~~`~`````~`~``~` 3
                4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4
                
                012345678901234567890123456789012
                1 2 3
                (In the real game, the chests are not visible in the ocean.)
                
                Press enter to continue...''')

        input('''When you drop a sonar device directly on a chest, you retrieve it and the other
                sonar devices update to show how far away the next nearest chest is. The chests
                are beyond the range of the sonar device on the left, so it shows an X.
                
                1 2 3
                012345678901234567890123456789012
                
                0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
                1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
                2 `~`X``7`~~~~`C`~~~~`````~~``~~~`` 2
                3 ````````~~~`````~~~`~`````~`~``~` 3
                4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4
                
                012345678901234567890123456789012
                1 2 3
                
                The treasure chests don't move around. Sonar devices can detect treasure chests
                up to a distance of 9 spaces. Try to collect all 3 chests before running out of
                sonar devices. Good luck!
                
                Press enter to continue...''')

    @DeprecationWarning
    def setup(self):
        """
        Method to regulate setup of a new game file.
        :return:
        """
        self.new_file = True
        print('Would you like to view the instructions? (yes/no)')
        if input().lower().startswith('y'):
            self.show_instructions()
        print('How many sonar devices would you like?')
        self.devices = int(input())
        print('How many treasure chests should there be?')
        chests = int(input())
        # self.board = self.get_new_board()
        self.chests = self.get_random_chests(chests)
        self.previous_moves = []
        return

    @DeprecationWarning
    def delete(self):
        """
        Method to delete a game file properly.
        :return: Nothing.
        """
        while True:
            for subdir, dirs, files in os.walk(self.path):
                count = 0
                for file in files:
                    if file[len(file) - 3:len(file)] == 'snr':
                        count += 1
                        print(str(count) + '. ' + file)
            delete_game = input("Which game would you like to delete?\n")
            try:
                os.remove(self.path + '\\' + delete_game)
            except FileNotFoundError:
                try:
                    os.remove(self.path + '\\' + delete_game + ".snr")
                    pass
                except FileNotFoundError:
                    Loading.returning("That file was not found.", 1)
                    pass
            if input('Delete another file? "Yes" or "No".').lower() == 'yes':
                continue
            else:
                Loading.returning("The file was successfully deleted.", 2)
                return
        return

    def quit(self):
        """
        Method to regulate quitting the game and saving the game file.
        :return: Nothing.
        """
        if self.new_file:
            self.filename = input("File name?\n") + '.snr'
        board = chests = previous_moves = ''
        for i in self.board:
            for j in i:
                board += '{},'.format(j)
            board = '{}\t'.format(board[0:len(board) - 1])
        for i in self.chests:
            for j in i:
                chests += '{},'.format(j)
            chests = '{}\t'.format(chests[0:len(chests) - 1])
        for i in self.previous_moves:
            for j in i:
                previous_moves += '{},'.format(j)
            previous_moves = '{}\t'.format(previous_moves[0:len(previous_moves) - 1])
        try:
            game = open(self.path + '\\' + self.filename, 'w')
            game.write(Loading.caesar_encrypt("{}(G){}(G){}".format(str(self.devices), '(C)'.join([(','.join(str(j) for j in i)) for i in self.chests]),
                                                                    '(P)'.join([(','.join(str(j) for j in i)) for i in self.previous_moves]) + '\n')))
            # game.write(Loading.caesar_encrypt(board[0:len(board) - 1]) + '\n')
            # game.write(Loading.caesar_encrypt(chests[0:len(chests) - 1]) + '\n')
            # game.write(Loading.caesar_encrypt(previous_moves[0:len(previous_moves) - 1]) + '\n')
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)
        Loading.returning("Saving game progress...", 2)
