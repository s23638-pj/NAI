import numpy as np
from easyAI import TwoPlayerGame


class ConnectFour(TwoPlayerGame):
    def __init__(self, players, board=None):
        self.players = players
        self.board = (
            board
            if (board is not None)
            else (np.array([[0 for i in range(7)] for j in range(6)]))
        )
        self.current_player = 1  # Zaczyna gracz numer 1
        self.last_move = None  # Dodane pole do przechowywania informacji o ostatnim ruchu

    def show(self):
        colors = ["\u001b[0m", "\u001b[32m",
                  "\u001b[34m"]  # ANSI Escape Codes dla kolorów (0m - domyślny, 32m - zielony, 34m - niebieski)
        print("\n1 2 3 4 5 6 7")
        for row in range(6):
            row_str = ""
            for col in range(7):
                cell = self.board[5 - row][col]
                cell_color = colors[cell]
                row_str += f"{cell_color}{'O' if cell == 1 else 'X' if cell == 2 else '.'}\u001b[0m "
            print(row_str)

    def possible_moves(self):
        return [
            i + 1 for i in range(7)
            if (self.board[:, i].min() == 0)
        ]

    def make_move(self, column):
        column -= 1  # Odejmujemy 1, aby przekształcić od 1 do 7 na od 0 do 6
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.current_player
        self.last_move = (line, column, self.current_player)  # Zaktualizuj informacje o ostatnim ruchu

    def lose(self):
        return find_four(self.board, self.opponent_index)

    # -----------------

   def is_over(self):
	''' 
	Check if the game is over.
            
            Returns:
                bool: True if the game is over, False otherwise.
	'''
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
	''' 
	 Calculate the score of the current game state.
            
            Returns:
                int: The score of the current game state.
	'''
        return -100 if self.lose() else 0


def find_four(board, current_player):
	'''
	Check if there are four in a row for the given player.
            
            Parameters:
                board (numpy.ndarray): The game board.
                current_player (int): The current player (1 or 2).
            
            Returns:
                bool: True if there are four in a row, False otherwise. 
	'''
    for pos, direction in POS_DIR:
        if has_four_in_a_row(board, pos, direction, current_player):
            return True
    return False


def has_four_in_a_row(board, start_pos, direction, current_player):
	''' 
	Check if there are four in a row in a given direction.
            
            Parameters:
                board (numpy.ndarray): The game board.
                start_pos (tuple): Starting position for checking.
                direction (numpy.ndarray): Direction of checking.
                current_player (int): The current player (1 or 2).
            
            Returns:
                bool: True if there are four in a row, False otherwise.

	'''
    streak = 0
    while is_valid_position(start_pos):
	'''
	Check if a position is valid on the game board.
            
            Parameters:
                pos (tuple): The position to check.
            
            Returns:
                bool: True if the position is valid, False otherwise.
	'''
        if board[start_pos[0], start_pos[1]] == current_player:
            streak += 1
            if streak == 4:
                return True
        else:
            streak = 0
        start_pos = move_position(start_pos, direction)
    return False


def is_valid_position(pos):
	'''
	Check if a position is valid on the game board.
            
            Parameters:
                pos (tuple): The position to check.
            
            Returns:
                bool: True if the position is valid, False otherwise.
	'''
    return 0 <= pos[0] <= 5 and 0 <= pos[1] <= 6


def move_position(pos, direction):
	'''
	Move a position in a given direction.
            
            Parameters:
                pos (tuple): The current position.
                direction (numpy.ndarray): Direction of movement.
            
            Returns:
                tuple: New position after movement.
	'''
    return pos + direction
POS_DIR = np.array(
    # Pionowe kierunki
    [[[i, 0], [0, 1]] for i in range(6)]
    # Poziome kierunki
    + [[[0, i], [1, 0]] for i in range(7)]
    # Skosy w prawo (górna część planszy)
    + [[[i, 0], [1, 1]] for i in range(1, 3)]
    # Skosy w prawo (lewa część planszy)
    + [[[0, i], [1, 1]] for i in range(4)]
    # Skosy w lewo (górna część planszy)
    + [[[i, 6], [1, -1]] for i in range(1, 3)]
    # Skosy w lewo (prawa część planszy)
    + [[[0, i], [1, -1]] for i in range(3, 7)]
)

if __name__ == "__main__":

    from easyAI import AI_Player, Negamax, SSS, Human_Player

    ai_neg = Negamax(5)
    ai_sss = SSS(5)
    human = Human_Player
    game = ConnectFour([Human_Player(human), Human_Player(human)])
    game.play()

    if game.lose():
        print("Player %d wins." % game.opponent_index)
    else:
        print("We have a draw")

    # Wyświetlanie informacji o ostatnim ruchu po zakończeniu gry
    if game.last_move:
        line, column, player = game.last_move
        print(f"Last move: Player {player} in column {column + 1}, row {line + 1}.")
