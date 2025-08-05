"""
Sudoku Game, replicated in Python.
"""
import math

import random
from Applications.cabinet import FileEngine
from System import Loading


category = "games"
version = "1.5"
entries = ('sudoku', '4')


def boot(os_object=None):
    """
    Method to handle booting and quitting.
    :param os_object: Operating System object, used for the path variable.
    :return:
    """
    sudoku = Sudoku(os_object.path.format(os_object.current_user.username))
    if not sudoku.filename == "exit":
        sudoku.main()


class Sudoku:
    """
    Main class to hold all the methods and things.
    """

    def __init__(self, path):
        self.new_file = False
        self.filename = ''
        self.path = path
        self.N = 0
        self.K = 0
        self.SRN = 0
        self.solution = []
        game_info = FileEngine.init(self, self.path, 'sdu')
        if game_info:
            self.board = [[int(j) for j in i.split('.')] for i in game_info[0].split('\n')[0].split(',')]
            self.solution = [[int(j) for j in i.split('.')] for i in game_info[1].split(',')]

    def __repr__(self):
        return "{}(G){}".format((','.join('.'.join(str(j) for j in i) for i in self.board)), ','.join('.'.join(str(j) for j in i) for i in self.solution))

    def __getstate__(self):
        return ""

    def main(self):
        """
        The main application screen.
        :return: Nothing.
        """
        if self.new_file:
            self.setup()
        print("\nWelcome to Sudoku.")
        while not [all([all([j != 0 for j in i]) for i in self.board])][0]:
            print(Loading.colored("  1 2 3 4 5 6 7 8 9", "blue"))
            for i in self.board:
                print(Loading.colored(str(int(self.board.index(i)) + 1), "blue") + ' ' + ' '.join(str(j) if j != 0 else ' ' for j in i))
            coordinates, number = self.enter_player_move()
            if coordinates == 0 and number == 0:
                FileEngine.quit(self, ".sdu")
                return
            else:
                try:
                    if self.solution[coordinates[0]][coordinates[1]] == number:
                        Loading.returning(Loading.colored("Correct!", Loading.COLORS["green"]), 2)
                        self.board[int(coordinates[0])][int(coordinates[1])] = int(number)
                    else:
                        Loading.returning(Loading.colored("Incorrect!", Loading.COLORS["red"]))
                except (TypeError, ValueError):
                    Loading.returning("An error occurred.", 2)

    def setup(self):
        """
        Screen to set up a new game.
        :return:
        """
        print("Welcome to Sudoku!")
        if input("Would you like to view the instructions?").startswith('y'):
            input("Sudoku is a game of logic.\nThe goal is to fill the board with numbers. How, you might ask? There are a few simple rules. Press ENTER to continue.")
            input("Rule 1: Each box only has one of each number.\nRule 2: Each row only has one of each number\nRule 3: Each column only has one of each number.")
            input("There will be numbers provided at the beginning of each game. These cannot be changed.\nNo guessing is necessary. Every Sudoku puzzle can be solved with logic.")
        # Create a new board
        self.new_board(9, 20)
        for i in range(self.SRN):
            self.fill_box(3 * i, 3 * i)
        self.fill_remaining(0, self.SRN)
        self.solution = [i.copy() for i in self.board]
        self.remove_k_digits()
        return

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

    def unused_in_box(self, row_start, col_start, num):
        """
        Method to determine whether num is unused in the box specified
        :param row_start: Row to check
        :param col_start: Column to check
        :param num: Number to find
        :return: True if the number is not used, False if it is.
        """
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.board[row_start + i][col_start + j] == num:
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
        """
        Method to determine if a number is not used in a row.
        :param i: Row Number.
        :param num: The number to check.
        :return: True if the number is not used, False if it is.
        """
        for j in range(self.N):
            if self.board[i][j] == num:
                return False
        return True

    def unused_in_col(self, j, num):
        """
        Method to determine if a number is not used in a column.
        :param j: Column Number.
        :param num: The number to check.
        :return: True if the number is not used, False if it is.
        """
        for i in range(self.N):
            if self.board[i][j] == num:
                return False
        return True

    def fill_remaining(self, i, j):
        """
        Recursive method to fill the remaining squares.
        :param i: Row number.
        :param j: Column number.
        :return: True if out of bounds, False if the function finishes.
        """
        # System.out.println(i+" "+j)
        if j >= 9 and i < 9 - 1:
            i += 1
            j = 0
        if i >= 9 and j >= 9:
            return True

        if i < 3:
            if j < 3:
                j = 3
        elif i < 9 - 3:
            if j == (int(i / 3)) * 3:
                j += 3
        else:
            if j == 9 - 3:
                i += 1
                j = 0
                if i >= 9:
                    return True
        for num in range(1, self.N + 1):
            if self.check_if_safe(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0
        return False

    def remove_k_digits(self):
        """
        Removes K number of digits from the board.
        :return: Nothing.
        """
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

    def get_square(self, row, col, status='square'):
        """
        Returns an entire square of board data.
        :param row: The specified row.
        :param col: The specified column.
        :param status: This specifies whether to return a 3x3 or a 1x9 list matrix.
        :return: List matrix of the specified row and column.
        """
        if status == "list":
            return self.board[row * 3][col * 3: col * 3 + 3] + \
                   self.board[row * 3 + 1][col * 3: col * 3 + 3] + \
                   self.board[row * 3 + 2][col * 3: col * 3 + 3]
        elif status == "square":
            return [self.board[row * 3][col * 3: col * 3 + 3]] + \
                   [self.board[row * 3 + 1][col * 3: col * 3 + 3]] + \
                   [self.board[row * 3 + 2][col * 3: col * 3 + 3]]

    def enter_player_move(self):
        """
        Method to collect the player's move.
        :return: The player's move.
        """
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
