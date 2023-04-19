# Sure! Here's a basic outline for how you could implement Celestial War using Python:

# Define the Piece class: This class should define the properties and methods for each piece in the game. Each piece should have a type, position on the board, and method to calculate its valid moves.

# Define the Board class: This class should represent the game board and manage the movement of pieces. It should have a 10x10 matrix of Piece objects, with each position initialized to the appropriate type of piece. It should also have methods to check for valid moves, capture pieces, and check for checkmate.

# Define the Player class: This class should represent each player in the game and manage their turns. It should have a set of pieces and methods to move them and capture opponent pieces.

# Define the Game class: This class should manage the game flow and user interface. It should initialize the board and players, start the game loop, and prompt users for input.

# Implement the game flow: This includes managing turns, checking for valid moves and capturing pieces, checking for checkmate, and displaying the winner.

# Implement the Gravity Zones: Determine the effects of the various Gravity Zones and implement them in the Board class.

# Create a graphical user interface (GUI): Use a GUI toolkit such as tkinter to create a visual representation of the game board and allow users to interact with the game.

# Play the game: Run the program and let users play the game!

# Note that this is just a basic outline, and the specific implementation of each component will depend on your programming skills and the specific requirements of the game.

import tkinter as tk
from tkinter import messagebox

class GameGUI:
    def __init__(self):
        self.game = Game()
        self.window = tk.Tk()
        self.window.title("Celestial War")
        self.create_board()
        self.create_players()
        self.create_buttons()
        self.update_display()
        self.current_piece = None

    def create_board(self):
        self.board_frame = tk.Frame(self.window)
        self.board_frame.grid(row=0, column=0)
        self.squares = []
        for i in range(8):
            row = []
            for j in range(8):
                square = tk.Button(self.board_frame, width=2, height=1, command=lambda row=i, col=j: self.click_square(row, col))
                square.grid(row=i, column=j)
                row.append(square)
            self.squares.append(row)

    def create_players(self):
        self.players_frame = tk.Frame(self.window)
        self.players_frame.grid(row=0, column=1, sticky=tk.N)
        self.player1_label = tk.Label(self.players_frame, text=f"{self.game.players[0].name} ({self.game.players[0].color})")
        self.player1_label.pack()
        self.player1_captured_label = tk.Label(self.players_frame, text="Captured: ")
        self.player1_captured_label.pack()
        self.player2_label = tk.Label(self.players_frame, text=f"{self.game.players[1].name} ({self.game.players[1].color})")
        self.player2_label.pack()
        self.player2_captured_label = tk.Label(self.players_frame, text="Captured: ")
        self.player2_captured_label.pack()

    def create_buttons(self):
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.grid(row=1, column=0, columnspan=2, sticky=tk.N)
        self.quit_button = tk.Button(self.buttons_frame, text="Quit", command=self.window.quit)
        self.quit_button.pack(side=tk.RIGHT)
        self.new_game_button = tk.Button(self.buttons_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side=tk.LEFT)

    def update_display(self):
        for i in range(8):
            for j in range(8):
                piece = self.game.board.get_piece(i, j)
                if piece is None:
                    self.squares[i][j].config(text=" ")
                else:
                    self.squares[i][j].config(text=piece.piece_type)
                    if piece.color == "White":
                        self.squares[i][j].config(fg="black", bg="white")
                    else:
                        self.squares[i][j].config(fg="white", bg="black")
        self.player1_captured_label.config(text=f"Captured: {', '.join(self.game.players[0].captured)}")
        self.player2_captured_label.config(text=f"Captured: {', '.join(self.game.players[1].captured)}")
        self.player1_label.config(fg="black" if self.game.current_player_index == 0 else "gray")
        self.player2_label.config(fg="black" if self.game.current_player_index == 1 else "gray")

    def new_game(self):
        self.game = Game()
        self.update_display()
        self.current_piece = None

    def click_square(self, row, col):
        if self.current_piece is None:
            piece = self.game.board.get_piece(row, col)
            if piece is not None and piece.color == self.game.players[self.game.current_player_index]:
                moves = piece.valid_moves(self.game.board)
                if len(moves) > 0:
                    self.current_piece = piece
                    self.current_row = row
                    self.current_col = col
                    for move in moves:
                        self.squares[move[0]][move[1]].config(bg="yellow")
            else:
                self.current_piece = None
                self.update_display()
        elif (row, col) in self.current_piece.valid_moves(self.game.board):
            try:
                self.game.move_piece(self.current_row, self.current_col, row, col)
                self.update_display()
                if self.game.game_over:
                    winner = self.game.winner.name
                    messagebox.showinfo("Game Over", f"{winner} wins!")
                else:
                    self.current_piece = None
                    self.game.next_turn()
                    self.update_display()
                    if self.game.current_player.is_computer:
                        self.window.after(1000, self.computer_move)
            except ValueError:
                pass
        else:
            self.current_piece = None
            self.update_display()


    def computer_move(self):
        move = self.game.current_player.get_move(self.game.board)
        self.game.move_piece(move[0][0], move[0][1], move[1][0], move[1][1])
        self.update_display()
        if self.game.game_over:
            winner = self.game.winner.name
            messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            self.game.next_turn()
            self.update_display()
            if self.game.current_player.is_computer:
                self.window.after(1000, self.computer_move)

if __name__ == "__main__":
    GameGUI().window.mainloop()