"""
Module tictactoe. Contains the classes and methods for the TTT game.
"""
import os
import random
from System import Loading
from Applications import bagels


# noinspection PyTypeChecker
class Tictactoe:
    """
    Class Tictactoe. Contains the core code for the game.
    """
    category = "games"

    @staticmethod
    def boot(path='\\'):
        """
        Regulates the startup of the game.
        :param path: Path to the game files.
        :return: Nothing.
        """
        ttt = Tictactoe(path)
        if not ttt.filename == 'exit':
            ttt.main()

    def __init__(self, path="\\"):
        self.new_file = False
        self.filename = ''
        self.path = path
        game_info = bagels.init_game(self, path, 'ttt')
        if self.new_file:
            (self.board, self.turn, self.player_letter) = ([" "] * 9, "", "")
        elif game_info:
            (board, self.turn, self.player_letter) = game_info
            while ',' in board:
                board = board.split(',', 1)[0] + board.split(',', 1)[1]
            self.board = []
            for j in range(len(board)):
                self.board.append(board[j])
            if self.player_letter == 'X':
                self.computer_letter = 'O'
            else:
                self.computer_letter = 'X'
        return

    def __repr__(self):
        return "< I am a tictactoe class named " + self.__class__.__name__ + ">"

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
    def input_player_letter():
        """
        Lets the player type which letter they want to be.
        :return:  A list with the player's letter as the first item, and the computer's letter as the second.
        """
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('Do you want to be X or O?')
            letter = input().upper()

        # the first element in the tuple is the player's letter, the second is the computer's letter.
        if letter == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

    @staticmethod
    def who_goes_first():
        """
        Randomly choose the player who goes first.
        :return: Who goes first.
        """
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'

    @staticmethod
    @DeprecationWarning
    def make_move(board, letter, move):
        """
        Deprecated method to make the move on the board.
        :param board: Board to use.
        :param letter: Whose letter?
        :param move: Where on the board to make the move.
        :return: Nothing.
        """
        board[move] = letter

    @staticmethod
    def is_winner(board, letter):
        """
        Method used to check if a letter has won?
        :param board: Which board to check.
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

    @DeprecationWarning
    def get_board_copy(self):
        """
        Deprecated method to create a duplicate board.
        :return: The duplicate board
        """
        # Make a duplicate of the board list and return it.
        dupe_board = []

        for i in self.board:
            dupe_board.append(i)

        return dupe_board

    @staticmethod
    @DeprecationWarning
    def is_space_free(board, move):
        """
        Deprecated method to check if a spot is free on the board.
        :param board: Board to check.
        :param move: Where on the board to check.
        :return: True if the spot is free. False if it is not.
        """
        # Return true if the passed move is free on the passed board.
        return board[move] == ' '

    @staticmethod
    def get_player_move(board):
        """
        Method to collect the player's move.
        :param board: Board to play on.
        :return: The player's move.
        """
        # Let the player type in his move.
        while True:
            print('Enter your move from 1-9! Or type "exit" to exit.')
            move = input()
            if move in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                if board[int(move)-1] == ' ':
                    return int(move)-1
                else:
                    print("That move is taken!")
            elif move in ('quit', 'exit', 'get me out of here'):
                return 'quit'

    @staticmethod
    def choose_random_move_from_list(board, moves_list):
        """
        Method to choose random moves from a specific given list.
        :param board: Board to choose from.
        :param moves_list: Specific list of moves given.
        :return: The random move.
        """
        # Returns a valid move from the passed list on the passed board.
        # Returns None if there is no valid move.
        possible_moves = []
        for i in moves_list:
            if board[i] == ' ':
                possible_moves.append(i)

        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        else:
            return None

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
                copy[i] = self.computer_letter
                # self.make_move(copy, player_letter, i)
                if self.is_winner(copy, player_letter):
                    return i

        # Try to take one of the corners, if they are free.
        move = self.choose_random_move_from_list(self.board, [0, 2, 6, 8])
        if move is not None:
            return move

        # Try to take the center, if it is free.
        if self.board[4] == ' ':
            return 4

        # Move on one of the sides.
        return self.choose_random_move_from_list(self.board, [1, 3, 5, 7])

    def is_board_full(self):
        """
        Method to find out whether the board is full.
        :return: True if every space on the board has been taken. Otherwise, return False.
        """
        for i in range(1, 9):
            if self.board[i] == ' ':
                return False
        return True

    @DeprecationWarning
    def delete(self):
        """
        Method to regulate deletion of game files.
        :return:
        """
        while True:
            for subdir, dirs, files in os.walk(self.path):
                count = 0
                for file in files:
                    if file[len(file)-3:len(file)] == 'ttt':
                        count += 1
                        print(str(count) + '. ' + file)
            delete_game = input("Which game would you like to delete?\n")
            try:
                os.remove(self.path + '\\' + delete_game)
            except FileNotFoundError:
                try:
                    os.remove(self.path + '\\' + delete_game + ".ttt")
                    pass
                except FileNotFoundError:
                    Loading.returning("That file was not found.", 1)
                    pass
            if input('Delete another file? "Yes" or "No".').lower() == 'yes':
                continue
            else:
                Loading.returning("The file was successfully deleted.", 2)
                return

    @staticmethod
    def startup(turn):
        """
        Method to regulate startup of an existing game.
        :param turn: Whose turn?
        :return: Nothing.
        """
        print("Welcome back!")
        if turn == 'player':
            print("It is your turn. Here is your board:")
            pass
        else:
            print("It is the computer's turn. Press [ENTER] or [return] to continue.")
            input()
            pass
        return

    def quit(self):
        """
        Method to quit the game and save progress.
        :return: Nothing.
        """
        translated_board = ','.join(self.board)
        if self.new_file:
            self.filename = input("File name?\n") + '.ttt'
        try:
            game = open(self.path + "\\" + self.filename, 'w')
            game.write(Loading.caesar_encrypt("{}\t{}\t{}".format(translated_board, self.turn, self.player_letter)))
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)

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
        if self.turn == '' or self.player_letter == '':
            empty = True
        if not empty:
            if self.player_letter == 'X':
                self.computer_letter = 'O'
            else:
                self.computer_letter = 'X'
            self.startup(self.turn)
        else:
            self.player_letter, self.computer_letter = self.input_player_letter()
            self.turn = self.who_goes_first()

        while True:
            game_is_playing = True
            print('The ' + self.turn + ' will go first.')

            while game_is_playing:
                if self.turn == 'player':
                    # Player's turn.
                    self.draw_board()
                    move = self.get_player_move(self.board)
                    if move in ('exit', 'quit', 'get me out of here'):
                        # Safely quit the app.
                        self.quit()
                        Loading.returning("Saving game progress...", 2)
                        return
                    else:
                        self.board[int(move)] = self.player_letter
                        # self.make_move(self.board, self.player_letter, int(move))
                    if self.is_winner(self.board, self.player_letter):
                        self.draw_board()
                        print('Hooray! You have won the game!')
                        game_is_playing = False
                    else:
                        if self.is_board_full():
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
                        game_is_playing = False
                    else:
                        if self.is_board_full():
                            self.draw_board()
                            print('The game is a tie!')
                            break
                        else:
                            self.turn = 'player'

            os.remove(self.path + self.filename)
            print('Do you want to play again? (yes or no)')
            if input().lower().startswith('y'):
                (self.board, self.turn, self.player_letter) = ([" "] * 9, "", "")
                self.new_file = True
            else:
                Loading.returning_to_apps()
                return
