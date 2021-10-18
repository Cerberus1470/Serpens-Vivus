import time
import random


class TicTacToe:

    def __init__(self):
        return

    def __repr__(self):
        return "< I am a tictactoe class named " + self.__class__.__name__ + ">"

    def draw_board(self, board):
        # This function prints out the board that it was passed.

        # "board" is a list of 10 strings representing the board (ignore index 0)
        print('   |   |')
        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
        print('   |   |')

    def input_player_letter(self):
        # Lets the player type which letter they want to be.
        # Returns a list with the player's letter as the first item, and the computer's letter as the second.
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('Do you want to be X or O?')
            letter = input().upper()

        # the first element in the tuple is the player's letter, the second is the computer's letter.
        if letter == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

    def who_goes_first(self):
        # Randomly choose the player who goes first.
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'

    def play_again(self):
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')

    def make_move(self, board, letter, move):
        board[move] = letter

    def is_winner(self, bo, le):
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
                (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
                (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
                (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
                (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
                (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
                (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
                (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal

    def get_board_copy(self, board):
        # Make a duplicate of the board list and return it the duplicate.
        dupe_board = []

        for i in board:
            dupe_board.append(i)

        return dupe_board

    def is_space_free(self, board, move):
        # Return true if the passed move is free on the passed board.
        return board[move] == ' '

    def get_player_move(self, board):
        # Let the player type in his move.
        move = ' '
        while True:
            print('Enter your move from 1-9!')
            move = input()
            if move in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                if self.is_space_free(board, int(move)):
                    return int(move)
                else:
                    print("That move is taken!")
            if move in ('quit', 'exit', 'get me out of here'):
                return move

    def choose_random_move_from_list(self, board, moves_list):
        # Returns a valid move from the passed list on the passed board.
        # Returns None if there is no valid move.
        possible_moves = []
        for i in moves_list:
            if self.is_space_free(board, i):
                possible_moves.append(i)

        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        else:
            return None

    def get_computer_move(self, board, computer_letter):
        # Given a board and the computer's letter, determine where to move and return that move.
        if computer_letter == 'X':
            player_letter = 'O'
        else:
            player_letter = 'X'

        # Here is our algorithm for our Tic Tac Toe AI:
        # First, check if we can win in the next move
        for i in range(1, 10):
            copy = self.get_board_copy(board)
            if self.is_space_free(copy, i):
                self.make_move(copy, computer_letter, i)
                if self.is_winner(copy, computer_letter):
                    return i

        # Check if the player could win on his next move, and block them.
        for i in range(1, 10):
            copy = self.get_board_copy(board)
            if self.is_space_free(copy, i):
                self.make_move(copy, player_letter, i)
                if self.is_winner(copy, player_letter):
                    return i

        # Try to take one of the corners, if they are free.
        move = self.choose_random_move_from_list(board, [1, 3, 7, 9])
        if move is not None:
            return move

        # Try to take the center, if it is free.
        if self.is_space_free(board, 5):
            return 5

        # Move on one of the sides.
        return self.choose_random_move_from_list(board, [2, 4, 6, 8])

    def is_board_full(self, board):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if self.is_space_free(board, i):
                return False
        return True

    def quit(self, board):
        # Save game status to memory.
        print("Saving game progress...")
        saved_board = self.get_board_copy(board)
        time.sleep(3)
        return saved_board

    def main(self, stats, board, turn, player_letter):
        stats['tictactoe'] = 'running'
        print('Welcome to Tic Tac Toe!')

        while True:
            # Use the previous board!
            the_board = board
            empty = True
            for i in range(len(the_board)):
                empty = empty and the_board[i] == ' '
            if empty:
                player_letter, computer_letter = self.input_player_letter()
                turn = self.who_goes_first()
                print('The ' + turn + ' will go first.')
            else:
                player_letter = player_letter
                if player_letter == 'X':
                    computer_letter = 'O'
                else:
                    computer_letter = 'X'

            game_is_playing = True

            while game_is_playing:
                if turn == 'player':
                    # Player's turn.
                    self.draw_board(the_board)
                    move = self.get_player_move(the_board)
                    if move in ('exit', 'quit', 'get me out of here'):
                        # Safely quit the app.
                        return self.quit(the_board), turn, player_letter
                    self.make_move(the_board, player_letter, int(move))

                    if self.is_winner(the_board, player_letter):
                        self.draw_board(the_board)
                        print('Hooray! You have won the game!')
                        game_is_playing = False
                    else:
                        if self.is_board_full(the_board):
                            self.draw_board(the_board)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'computer'

                else:
                    # Computer's turn.
                    move = self.get_computer_move(the_board, computer_letter)
                    self.make_move(the_board, computer_letter, move)

                    if self.is_winner(the_board, computer_letter):
                        self.draw_board(the_board)
                        print('The computer has beaten you! You lose.')
                        game_is_playing = False
                    else:
                        if self.is_board_full(the_board):
                            self.draw_board(the_board)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'player'

            if self.play_again():
                board = [' '] * 10
            else:
                break
        return board, turn, player_letter
