"""
Module tictactoe. Contains the classes and methods for the TTT game.
"""
import os
import random
from System import Loading
from Applications import bagels


category = "games"
version = "2.1"
entries = ('tictactoe', 'tic-tac-toe', 'ttt', '4')


def boot(os_object=None):
    """
    Regulates the startup of the game.
    :param os_object: Operating System object, used for the path variable.
    :return: Nothing.
    """
    while True:
        ttt = Tictactoe(os_object.path.format(os_object.current_user.username))
        if not ttt.filename == 'exit':
            if not ttt.main() == "again":
                return
        else:
            return


# noinspection PyTypeChecker
class Tictactoe:
    """
    Class Tictactoe. Contains the core code for the game.
    """

    def __init__(self, path="\\", game_info=""):
        self.new_file = False
        self.filename = ''
        self.path = path
        if not game_info:
            game_info = bagels.init_game(self, path, 'ttt')
        if self.new_file:
            (self.board, self.turn, self.player_letter) = ([" "] * 9, "", "")
        elif game_info:
            (board, self.turn, self.player_letter) = game_info
            self.board = board.split(',')
            # while ',' in board:
            #     board = board.split(',', 1)[0] + board.split(',', 1)[1]
            # self.board = []
            # for j in range(len(board)):
            #     self.board.append(board[j])
            self.computer_letter = 'O' if self.player_letter == 'X' else 'X'
            self.new_file = True if self.filename == '' else False
        return

    def __repr__(self):
        return "{}(G){}(G){}".format(','.join(self.board), self.turn, self.player_letter)

    def __getstate__(self):
        return "Tictactoe(SS1){}(SS2){}(SS2){}".format(','.join(self.board), self.turn, self.player_letter)

    def main(self):
        """
        The main application screen.
        :return: Nothing.
        """
        print('Welcome to Tic Tac Toe!')
        # Use the previous values!
        empty = True
        for i in range(len(self.board)):
            empty = empty and self.board[i] == ''
        if all([i == ' ' for i in self.board]):
            self.player_letter = ""
            while not (self.player_letter == 'X' or self.player_letter == 'O'):
                print('Do you want to be X or O?')
                self.player_letter = input().upper()
            self.turn = "player"
            # random.choice(["player", "computer"])
            print('The ' + self.turn + ' will go first.')
        else:
            self.startup()
        self.computer_letter = 'O' if self.player_letter == 'X' else 'X'
        while True:
            if self.turn == 'player':
                # Player's turn.
                self.draw_board()
                move = self.get_player_move()
                if move in ('exit', 'quit', 'get me out of here'):
                    # Safely quit the app.
                    bagels.quit_game(self)
                    Loading.returning("Saving game progress...", 2)
                    return
                else:
                    self.board[int(move)] = self.player_letter
                    # self.make_move(self.board, self.player_letter, int(move))
                if self.is_winner(self.board, self.player_letter):
                    self.draw_board()
                    print('Hooray! You have won the game!')
                    break
                else:
                    if all([self.board[i] != ' ' for i in range(0, 8)]):
                        self.draw_board()
                        print('The game is a tie!')
                        break
                    else:
                        self.turn = 'computer'

            else:
                # Computer's turn.
                # self.draw_board(self.board)
                move = self.get_computer_move()
                self.board[int(move)] = self.computer_letter
                # self.make_move(self.board, self.computer_letter, int(move))

                if self.is_winner(self.board, self.computer_letter):
                    self.draw_board()
                    print('The computer has beaten you! You lose.')
                    break
                else:
                    if all([self.board[i] != ' ' for i in range(0, 8)]):
                        self.draw_board()
                        print('The game is a tie!')
                        break
                    else:
                        self.turn = 'player'
        if not self.new_file:
            os.remove(self.path + self.filename)
        if Loading.pocs_input("Do you want to play again? (yes or no)", self).lower().startswith('y'):
            return "again"
        else:
            Loading.returning_to_apps()
            return

    def startup(self):
        """
        Method to regulate startup of an existing game.
        :return: Nothing.
        """
        print("Welcome back!")
        if self.turn == 'player':
            print("It is your turn. Here is your board:")
            pass
        else:
            print("It is the computer's turn. Press [ENTER] or [return] to continue.")
            Loading.pocs_input(app_object=self)
            pass
        return

    def draw_board(self):
        """
        This function prints out the board that it was passed.
        :return: Nothing.
        """
        for i in range(3):
            print('   |   |')
            print(' ' + self.board[i * 3] + ' | ' + self.board[i * 3 + 1] + ' | ' + self.board[i * 3 + 2])
            print('   |   |')
            if not i == 2:
                print('-----------')
        print()

    @staticmethod
    def is_winner(board, letter):
        """
        Method used to check if a letter has won?
        :param board: Which board to check. Must be specified if we are looking at the original board
        :param letter: Whose letter?
        :return:
        """
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter, so we don't have to type as much.
        return ((board[6] == letter and board[7] == letter and board[8] == letter) or  # across the top
                (board[3] == letter and board[4] == letter and board[5] == letter) or  # across the middle
                (board[0] == letter and board[1] == letter and board[2] == letter) or  # across the bottom
                (board[6] == letter and board[3] == letter and board[0] == letter) or  # down the left side
                (board[7] == letter and board[4] == letter and board[1] == letter) or  # down the middle
                (board[8] == letter and board[5] == letter and board[2] == letter) or  # down the right side
                (board[6] == letter and board[4] == letter and board[2] == letter) or  # diagonal
                (board[8] == letter and board[4] == letter and board[0] == letter))  # diagonal

    def get_player_move(self):
        """
        Method to collect the player's move.
        :return: The player's move.
        """
        # Let the player type in his move.
        while True:
            print('Enter your move from 1-9! Or type "exit" to exit.')
            move = Loading.pocs_input(app_object=self)
            if move in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                if self.board[int(move) - 1] == ' ':
                    return int(move) - 1
                else:
                    print("That move is taken!")
            elif move in ('quit', 'exit', 'get me out of here'):
                return 'quit'

    def get_computer_move(self):
        """
        Method to collect a computer move.
        :return: The computer's move.
        """
        # Given a board and the computer's letter, determine where to move and return that move.
        if self.computer_letter == 'X':
            player_letter = 'O'
        else:
            player_letter = 'X'

        # Here is our algorithm for our Tic Tac Toe AI:
        # First, check if we can win in the next move
        for i in range(1, 9):
            copy = self.board.copy()
            if copy[i] == ' ':
                copy[i] = self.computer_letter
                # self.make_move(copy, self.computer_letter, i)
                if self.is_winner(copy, self.computer_letter):
                    return i

        # Check if the player could win on his next move, and block them.
        for i in range(1, 9):
            copy = self.board.copy()
            if copy[i] == ' ':
                copy[i] = self.player_letter
                # self.make_move(copy, player_letter, i)
                if self.is_winner(copy, player_letter):
                    return i

        # Try to take one of the corners, if they are free.
        try:
            return random.choice([i for i in [0, 2, 6, 8] if self.board[i] == ' '])
        except IndexError:
            pass

        # Try to take the center, if it is free.
        if self.board[4] == ' ':
            return 4

        # Move on one of the sides.
        return random.choice([i for i in [1, 3, 5, 7] if self.board[i] == ' '])
