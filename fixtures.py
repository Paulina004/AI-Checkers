import pytest
from p1_pdevito2019 import Checker
from easyAI import Human_Player, AI_Player, Negamax

@pytest.fixture
def checker_game():
    ai = Negamax(13) # The AI will think 13 moves in advance
    game = Checker( [ Human_Player(), AI_Player(ai) ] )
    return game

@pytest.fixture
def black_pieces():
    return [
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]

@pytest.fixture
def white_pieces():
    return [
        (6,1), (6,3), (6,5), (6,7),
        (7,0), (7,2), (7,4), (7,6)
        ]

@pytest.fixture
def black_squares():
    even = [0,2,4,6]
    odd = [1,3,5,7]

    even_row = [(i,j) for i in even for j in odd]
    odd_row = [(i,j) for i in odd for j in even]

    black_squares = even_row + odd_row
    return black_squares
