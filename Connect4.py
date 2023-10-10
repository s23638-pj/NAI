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
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0


def find_four(board, current_player):
    # Iteracja przez wszystkie możliwe kierunki w poszukiwaniu sekwencji czterech pionków
    for pos, direction in POS_DIR:
        # Sprawdzenie, czy w danym kierunku istnieje sekwencja czterech pionków
        if has_four_in_a_row(board, pos, direction, current_player):
            # Jeśli znaleziono sekwencję czterech pionków, zwróć True
            return True
    # Jeśli nie znaleziono sekwencji czterech pionków w żadnym kierunku, zwróć False
    return False


def has_four_in_a_row(board, start_pos, direction, current_player):
    # Inicjalizacja licznika dla śledzenia sekwencji czterech pionków
    streak = 0
    # Sprawdzenie kolejnych pozycji w danym kierunku
    while is_valid_position(start_pos):
        # Sprawdzenie, czy pionek na danej pozycji należy do aktualnego gracza
        if board[start_pos[0], start_pos[1]] == current_player:
            # Zwiększenie licznika, jeśli pionek należy do aktualnego gracza
            streak += 1
            # Jeśli znaleziono sekwencję czterech pionków, zwróć True
            if streak == 4:
                return True
        else:
            # Jeśli przerwano sekwencję, zresetuj licznik
            streak = 0
        # Przesunięcie do kolejnej pozycji w danym kierunku
        start_pos = move_position(start_pos, direction)
    # Jeśli nie znaleziono sekwencji czterech pionków w danym kierunku, zwróć False
    return False


def is_valid_position(pos):
    # Sprawdzenie, czy pozycja znajduje się w granicach planszy
    return 0 <= pos[0] <= 5 and 0 <= pos[1] <= 6


def move_position(pos, direction):
    # Przesunięcie pozycji o krok w danym kierunku
    return pos + direction


# Definicja wszystkich możliwych kierunków do sprawdzenia
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
