import pytest
from celestial_war import GameBoard
from celestial_war import Piece
from celestial_war import King
from celestial_war import Queen
from celestial_war import Star
from celestial_war import Comet
from celestial_war import Nebula
from celestial_war import Asteroid


# def test_game_board_initialization():
#     game_board = GameBoard()
#     assert len(game_board.board) == 10
#     assert len(game_board.board[0]) == 10

def test_initial_game_state():
    game_board = GameBoard()

    # Test placement of Asteroids
    for i in range(10):
        assert isinstance(game_board.get_piece((i, 1)), Asteroid)
        assert game_board.get_piece((i, 1)).color == "black"
        assert isinstance(game_board.get_piece((i, 8)), Asteroid)
        assert game_board.get_piece((i, 8)).color == "white"

    # Test placement of other pieces
    pieces = [
        (Nebula, 0),
        (Comet, 1),
        (Star, 2),
        (Queen, 3),
        (King, 4),
        (Star, 5),
        (Comet, 6),
        (Nebula, 7),
    ]

    for piece_class, index in pieces:
        assert isinstance(game_board.get_piece((index, 0)), piece_class)
        assert game_board.get_piece((index, 0)).color == "black"
        assert isinstance(game_board.get_piece((index, 9)), piece_class)
        assert game_board.get_piece((index, 9)).color == "white"

    # Test empty squares
    for row in range(2, 8):
        for col in range(10):
            assert game_board.is_empty_square((col, row))


# def test_piece_movement():
#     piece = Piece((0, 0), "white")
#     piece.move((1, 1))
#     assert piece.position == (1, 1)

def test_king_movement():
    game_board = GameBoard()
    king = King((4, 4), "white")
    game_board.board[4][4] = king

    # Test valid move
    captured_piece = game_board.move_piece(king, (4, 5))
    assert captured_piece is None
    assert game_board.get_piece((4, 5)) == king
    assert game_board.is_empty_square((4, 4)) == True

    # Test invalid move
    with pytest.raises(ValueError):
        game_board.move_piece(king, (4, 7))

def test_queen_movement():
    game_board = GameBoard()
    queen = Queen((4, 4), "white")
    game_board.board[4][4] = queen

    # Test valid move
    captured_piece = game_board.move_piece(queen, (7, 7))
    assert captured_piece is None
    assert game_board.get_piece((7, 7)) == queen
    assert game_board.is_empty_square((4, 4)) == True

    # Test invalid move
    invalid_new_position = (2, 6)
    with pytest.raises(ValueError):
        game_board.move_piece(queen, invalid_new_position)


def test_star_movement():
    game_board = GameBoard()
    star = Star((4, 4), "white")
    game_board.board[4][4] = star

    # Test valid move
    captured_piece = game_board.move_piece(star, (5, 5))
    assert captured_piece is None
    assert game_board.get_piece((5, 5)) == star
    assert game_board.is_empty_square((4, 4)) == True

    # Add an obstacle in the path
    obstacle = Piece((4, 6), "white")
    game_board.board[4][6] = obstacle

    # Test invalid move
    invalid_new_position = (4, 7)
    with pytest.raises(ValueError):
        game_board.move_piece(star, invalid_new_position)



def test_comet_movement():
    game_board = GameBoard()
    comet = Comet((4, 4), "white")
    game_board.board[4][4] = comet

    # Test valid move
    captured_piece = game_board.move_piece(comet, (4, 7))
    assert captured_piece is None
    assert game_board.get_piece((4, 7)) == comet
    assert game_board.is_empty_square((4, 4)) == True

    # Test invalid move
    with pytest.raises(ValueError):
        game_board.move_piece(comet, (2, 7))


def test_nebula_movement():
    game_board = GameBoard()
    nebula = Nebula((4, 4), "white")
    game_board.board[4][4] = nebula

    # Test valid move
    captured_piece = game_board.move_piece(nebula, (4, 6))
    assert captured_piece is None
    assert game_board.get_piece((4, 6)) == nebula
    assert game_board.is_empty_square((4, 4)) == True

    # Test invalid move
    with pytest.raises(ValueError):
        game_board.move_piece(nebula, (2, 2))

def test_asteroid_movement():
    game_board = GameBoard()
    asteroid = Asteroid((4, 4), "white")
    enemy_piece = Piece((5, 5), "black")
    game_board.board[5][5] = enemy_piece
    game_board.board[4][4] = asteroid

    captured_piece = game_board.move_piece(asteroid, (6, 6))
    assert captured_piece == enemy_piece
    assert game_board.get_piece((6, 6)) == asteroid
    assert game_board.is_empty_square((4, 4)) == True
