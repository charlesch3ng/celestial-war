# main.py

from board import Board
from game import Game
from player import Player
from piece import Piece
from gui import GameGUI

# create the game board and pieces
board = Board()
pieces = board.initiate()

# create the players
player1 = Player("Player 1", "white")
player2 = Player("Player 2", "black")

# create the game
game = Game(board, [player1, player2], pieces)

# create and run the GUI
gui = GameGUI(game)
gui.run()