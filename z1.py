"""
Poniższy kod zawiera implementację zasad gry Connect4/Czwórki.
Zasady gry: https://pl.wikipedia.org/wiki/Czw%C3%B3rki
Wykonane przez: Dawid Nowakowski i Michał Krokoszyński

Instrukcja przygotowania środowiska 

________________________________________
----------INSTALACJA PYTHON-------------
________________________________________

Windows:
1. Ze strony python.org/downloads pobierz najnowszą wersję Pythona dla systemu Windows.
2. Uruchom instalator, zaznacz "Add Python to PATH".
3. Kliknij "Install Now".

macOS:
0. Jeśli nie posiadasz Homebrew, w terminalu:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
1. Wykonaj w terminalu: brew install python

Linux (Ubuntu/Debian):
W terminalu wpisz:

1. sudo apt update
2. sudo apt install python3 python3-pip

________________________________________
--INSTALACJA EASYAI I URUCHOMIENIE GRY--
________________________________________

1. W terminalu wykonaj: pip install easyAI
2. Przejdź w terminalu do katalogu zawierającego plik z grą z Connect4/Czwórki
3. Wykonaj: python z1.py
* z1.py = nazwa pliku z grą Connect4/Czwórki
"""

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

def MakeEmptyBoard():

    """
    Tworzy pustą planszę do gry.
    Wymiary planszy: 6wierszy x 7kolumn, poćzątkowo każde pole jest oznaczone znakiem "O"
    """

    return [["O" for _ in range(7)] for _ in range(6)]

class Connect4(TwoPlayerGame):

    """
    Implementacja gry używając easyAI
    """

    def __init__(self, players=None):
        """
        Inicjalizacja gry

        players - lista graczy
        board - tworzy pustą planszę do gry korzystając z funkcji MakeEmptyBoard()
        curret_player - ustawia bieżącego gracza na 1
        """
        self.players = players
        self.board = MakeEmptyBoard()
        self.current_player = 1

    def possible_moves(self):
        """
        Zwraca listę możliwych ruchów - wybór umieszczenia żetona w kolumnach 1-7
        """
        return [str(i + 1) for i in range(7) if self.board[0][i] == "O"]

    def make_move(self, move):
        """
        Wykonuje ruch gracza na podstawie wybranej kolumny tj. agrumentu "move"
        W wybranej kolumnie wstawia żeton w rzędzie, w którym nie ma żadnego żetonu licząc od dołu.
        Żeton gracza nr 1 = #
        Żeton gracza nr 2 = X
        """
        col = int(move) - 1
        mark = "#" if self.current_player == 1 else "X"
        
        for i in range(5, -1, -1):
            if self.board[i][col] == "O":
                self.board[i][col] = mark
                break

    def win(self):

        """
        Sprawdza, czy któryś z graczy wygrał grę zwracając "True".
        Możliwe wygrane to ułożenie 4 żetonów:
        - poziomo
        - pionowo
        - po porzekątnych
        """

        for i in range(6):
            for j in range(4):
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] != "O":
                    return True
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] != "O":
                    return True
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] != "O":
                    return True
        for i in range(3, 6):
            for j in range(4):
                if self.board[i][j] == self.board[i-1][j+1] == self.board[i-2][j+2] == self.board[i-3][j+3] != "O":
                    return True
        return False

    def is_over(self):

        """
        Sprawdza czy gra zakończyła się, tj. czy któryś z graczy wygrał, lub nie ma możliwości nowych ruchów - plansza jest pełna.
        """

        return self.win() or all(self.board[0][col] != "O" for col in range(7))

    def show(self):

        """
        Wyświetla aktualny stan gry
        """

        for row in self.board:
            print(" ".join(row))
        print("1 2 3 4 5 6 7")
        print()

    def scoring(self):
        """
        Zwraca wynik dla AI
        Wygrana - 100pkt
        Przegrana - 0pkt
        """
        return 100 if self.win() else 0

ai = Negamax(7)
game = Connect4([Human_Player(), AI_Player(ai)])
history = game.play()