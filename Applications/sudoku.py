"""
Sudoku Game, replicated in Python.
"""
import math

import random
from Applications import bagels
from System import Loading
from termcolor import colored


class Sudoku:
    """
    Main class to hold all the methods and things.
    """
    category = "games"
    @staticmethod
    def boot(path='\\'):
        """
        Method to handle booting and quitting.
        :param path: Path to save/read files.
        :return:
        """
        sudoku = Sudoku(path)
        if not sudoku.filename == "exit":
            sudoku.main()

    def __init__(self, path):
        self.new_file = False
        self.filename = ''
        self.path = path
        self.N = 0
        self.K = 0
        self.SRN = 0
        self.solution = []
        game_info = bagels.init_game(self, self.path, 'sdu')
        if game_info:
            self.board = [[int(j) for j in i.split('.')] for i in game_info[0].split('\n')[0].split(',')]
            self.solution = [[int(j) for j in i.split('.')] for i in game_info[1].split(',')]


    def new_board(self, n, k):
        """
        Method to make a new board.
        :param n: Number of rows/columns.
        :param k: Number of digits to remove.
        :return: Nothing.
        """
        self.N = n
        self.K = k

        SRNd = math.sqrt(n)
        self.SRN = int(SRNd)

        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def unused_in_box(self, rowstart, colstart, num):
        """
        Method to determine whether num is unused in the box specified
        :param rowstart: Row to check
        :param colstart: Column to check
        :param num: Number to find
        :return: True if the number is not used, False if it is.
        """
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.board[rowstart + i][colstart + j] == num:
                    return False
        return True

    def fill_box(self, row, col):
        """
        Method to fill a box with random numbers
        :param row: Row of box
        :param col: Column of box
        :return: Nothing
        """
        for i in range(self.SRN):
            for j in range(self.SRN):
                num = random.randint(1, 9)
                while not self.unused_in_box(row, col, num):
                    num = random.randint(1, 9)
                self.board[row + i][col + j] = num

    def check_if_safe(self, i, j, num):
        """
        Method to check if num is safe to place. Combination of 3 methods
        :param i:
        :param j:
        :param num:
        :return:
        """
        return self.unused_in_row(i, num) and self.unused_in_col(j, num) and self.unused_in_box(i - i % self.SRN, j - j % self.SRN, num)

    def unused_in_row(self, i, num):
        for j in range(self.N):
            if self.board[i][j] == num:
                return False
        return True

    def unused_in_col(self, j, num):
        for i in range(self.N):
            if self.board[i][j] == num:
                return False
        return True

    def fill_remaining(self, i, j):
        # System.out.println(i+" "+j)
        if j >= 9 and i < 9 - 1:
            i = i + 1
            j = 0
        if (i >= 9 and j >= 9):
            return True

        if (i < 3):
            if (j < 3):
                j = 3
        elif (i < 9 - 3):
            if j == (int(i / 3)) * 3:
                j = j + 3
        else:
            if (j == 9 - 3):
                i = i + 1
                j = 0
                if (i >= 9):
                    return True
        for num in range(1, self.N + 1):
            if self.check_if_safe(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0
        return False

    def remove_k_digits(self):
        count = self.K
        while count != 0:
            cellID = random.randint(1, self.N * self.N - 1)
            i = int(cellID / self.N)
            j = cellID % 9
            if j != 0:
                j -= 1
            if self.board[i][j] != 0:
                count -= 1
                self.board[i][j] = 0

    def get_row(self, row):
        return self.board[row]

    def get_column(self, column):
        return [self.board[i][column] for i in range(len(self.board))]

    def get_square(self, row, col, status='square'):
        if status == "list":
            return self.board[row * 3][col * 3: col * 3 + 3] + \
                   self.board[row * 3 + 1][col * 3: col * 3 + 3] + \
                   self.board[row * 3 + 2][col * 3: col * 3 + 3]
        elif status == "square":
            return [self.board[row * 3][col * 3: col * 3 + 3]] + \
                   [self.board[row * 3 + 1][col * 3: col * 3 + 3]] + \
                   [self.board[row * 3 + 2][col * 3: col * 3 + 3]]

    def get_value_square(self, sqrow, sqcol, row, col):
        square = self.get_square(sqrow, sqcol)
        return square[row][col]

    def set_value_square(self, sqrow, sqcol, row, col, value):
        self.board[sqrow * 3 + row][sqcol * 3 + col] = value
        return

    def full(self, row=None, col=None):
        # full_board = [[False] * 3] * 3
        # if row and col:
        #     square = self.get_square(row, col)
        #     for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        #         if k not in square:
        #             return False
        #     else:
        #         return True
        # for i in range(0, 3):
        #     for j in range(0, 3):
        #         square = self.get_square(0, 0)
        #         for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        #             if k not in square:
        #                 break
        #         else:
        #             full_board[i][j] = True
        return [all([all([j != 0 for j in i]) for i in self.board])]

    def enter_player_move(self):
        while True:
            coordinates = input("Enter a coordinate by giving the row and the column, separated by a space. Type \"exit\" to exit.").split()
            if 'exit' in coordinates or 'quit' in coordinates or 'bruh' in coordinates:
                return 0, 0
            if len(coordinates) != 2:
                print("Make sure the numbers are separated by a space.")
                continue
            elif coordinates[0] not in '0123456789' or coordinates[1] not in '0123456789':
                print("Make sure you typed numbers.")
                continue
            coordinates = [int(i) - 1 for i in coordinates]
            if self.board[coordinates[0]][coordinates[1]] != 0:
                print("Select a spot with a 0.")
                continue
            else:
                break
        while True:
            number = input("Input the number you would like to place at {}, {}. Type \"exit\" to exit.".format(str(coordinates[0] + 1), str(coordinates[1] + 1)))
            if number in ("exit", "quit", "bruh"):
                return 0, 0
            if number not in '0123456789':
                print("Enter a number.")
                continue
            else:
                break
        return coordinates, int(number)

    def main(self):
        if self.new_file:
            self.setup()
        print("\nWelcome to Sudoku.")
        while not [all([all([j != 0 for j in i]) for i in self.board])][0]:
            print(colored("  1 2 3 4 5 6 7 8 9", "blue"))
            for i in self.board:
                print(colored(str(int(self.board.index(i)) + 1), "blue") + ' ' + ' '.join(str(j) if j != 0 else ' ' for j in i))
            coordinates, number = self.enter_player_move()
            if coordinates == 0 and number == 0:
                self.quit()
                return
            else:
                try:
                    if self.solution[coordinates[0]][coordinates[1]] == number:
                        Loading.returning(colored("Correct!", "green"), 2)
                        self.board[int(coordinates[0])][int(coordinates[1])] = int(number)
                    else:
                        Loading.returning(colored("Incorrect!", "red"))
                except (TypeError, ValueError):
                    Loading.returning("An error occurred.", 2)

    def setup(self):
        print("Welcome to Sudoku!")
        if input("Would you like to view the instructions?").startswith('y'):
            input("Sudoku is a game of logic.\nThe goal is to fill the board with numbers. How, you might ask? There are a few simple rules. Press ENTER to continue.")
            input("Rule 1: Each box only has one of each number.\nRule 2: Each row only has one of each number\nRule 3: Each column only has one of each number.")
            input("There will be numbers provided at the beginning of each game. These cannot be changed.\nNo guessing is necessary. Every Sudoku puzzle can be solved with logic.")
        # [[str(random.randint(1, 9)) for _ in range(9)] for _ in range(9)
        # Create a new board
        self.new_board(9, 20)
        for i in range(self.SRN):
            self.fill_box(3 * i, 3 * i)
        self.fill_remaining(0, self.SRN)
        self.solution = [i.copy() for i in self.board]
        self.remove_k_digits()
        # for i in range(0, 3):
        #     numbers = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
        #     for j in numbers:
        #         self.set_value_square(i, i, math.floor(numbers.index(j) / 3), numbers.index(j) % 3, j)
        # self.fillRemaining(0, 3)
        return
        # for h in range(1, 10):
        #     placements = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        #     for i in range(0, 3):
        #         for j in range(0, 3):
        #             while self.get_value_square(i, j, math.floor(placements[i][j] / 3), placements[i][j] % 3) != 0:
        #                 placements[i][j] = random.randint(0, 8)
        #             while h in self.get_row(math.floor(placements[i][j] / 3) + i * 3) or h in self.get_column((placements[i][j] % 3) + j * 3):
        #                 placements[i][j] = random.randint(0, 8)
        #             self.set_value_square(i, j, math.floor(placements[i][j] / 3), placements[i][j] % 3, h)
        # if not self.full():
        #     for i in range(0, 3):
        #         for j in range(0, 3):
        #             if not self.full(i, j):
        #                 missing = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        #                 for k in range(0, 9):
        #                     try:
        #                         missing.pop(missing.index(self.get_value_square(i, j, math.floor(k / 3), k % 3)))
        #                     except ValueError:
        #                         continue
        #                 for k in missing:
        #                     for x in range(0, 9):
        #                         if self.get_value_square(i, j, math.floor(x / 3), x % 3) == 0:
        #                             if k not in self.get_row(math.floor(x / 3) + i * 3) and k not in self.get_column((x % 3) + j * 3):
        #                                 self.set_value_square(i, j, math.floor(x / 3), x % 3, k)
        #                 pass

        # two_placements = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9)
        # for i in range(len(self.board)):
        #     self.board[i][two_placements[i]] = 2 if self.board[i] == 0 else self.board[i]

    def quit(self):
        """
        Method to regulate quitting the game and saving the game file.
        :return: Nothing.
        """
        if self.new_file:
            self.filename = input("File name?\n") + '.sdu'
        board = chests = previous_moves = ''
        try:
            game = open(self.path + '\\' + self.filename, 'w')
            game.write(Loading.caesar_encrypt(','.join('.'.join(str(j) for j in i) for i in self.board)) + '\n')
            game.write(Loading.caesar_encrypt(','.join('.'.join(str(j) for j in i) for i in self.solution)))
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)
        Loading.returning("Saving game progress...", 2)
        return