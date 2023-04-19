class Game:
    def __init__(self, board, players, pieces, current_player_index=0):
        self.board = board
        self.players = players
        self.current_player_index = current_player_index
        self.game_over = False
        self.winner = None

        for piece in pieces:
            self.board.set_piece(int(piece.row), int(piece.col), piece)


    def start(self):
        self.place_pieces()
        while not self.game_over:
            self.play_turn()
        print(f"Game over! Winner: {self.winner}")

    def place_pieces(self):
        # Place white pieces
        self.board.set_piece(Piece('P', 0, 3), 0, 3)
        self.board.set_piece(Piece('M', 0, 4), 0, 4)
        self.board.set_piece(Piece('S', 0, 0), 0, 0)
        self.board.set_piece(Piece('S', 0, 7), 0, 7)
        self.board.set_piece(Piece('C', 1, 1), 1, 1)
        self.board.set_piece(Piece('C', 1, 6), 1, 6)
        self.board.set_piece(Piece('N', 2, 2), 2, 2)
        self.board.set_piece(Piece('N', 2, 5), 2, 5)
        self.board.set_piece(Piece('A', 1, 4), 1, 4)
        # Place black pieces
        self.board.set_piece(Piece('P', 7, 4), 7, 4)
        self.board.set_piece(Piece('M', 7, 3), 7, 3)
        self.board.set_piece(Piece('S', 7, 0), 7, 0)
        self.board.set_piece(Piece('S', 7, 7), 7, 7)
        self.board.set_piece(Piece('C', 6, 1), 6, 1)
        self.board.set_piece(Piece('C', 6, 6), 6, 6)
        self.board.set_piece(Piece('N', 5, 2), 5, 2)
        self.board.set_piece(Piece('N', 5, 5), 5, 5)
        self.board.set_piece(Piece('A', 6, 4), 6, 4)

    def play_turn(self):
        print(self.board)
        player = self.players[self.current_player_index]
        print(f"{player}'s turn:")
        piece = self.get_player_move(player)
        if piece is None:
            self.game_over = True
            return
        moves = piece.valid_moves(self.board)
        end_row, end_col = self.get_player_move(player, moves)
        self.board.move_piece(piece.row, piece.col, end_row, end_col)
        if self.is_checkmate():
            self.game_over = True
            self.winner = self.players[self.current_player_index]
            return
        self.current_player_index = (self.current_player_index + 1) % 2

    def get_player_move(self, player, moves=None):
        while True:
            piece_input = input("Enter piece coordinates (row,col), or 'q' to quit: ")
            if piece_input.lower() == 'q':
                return None
            try:
                piece_row, piece_col = [int(x.strip()) for x in piece_input.split(',')]
                piece = self.board.get_piece(piece_row, piece_col)
                if piece is None or piece.color != player.color:
                    raise ValueError
                if moves is None:
                    return piece
                elif (piece.row, piece.col) in moves:
                    return piece
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input. Try again.")

        while True:
            move_input = input("Enter move coordinates (row,col): ")
            try:
                end_row, end_col = [int(x.strip()) for x in move_input.split(',')]
                if (end_row, end_col) in moves:
                    return end_row, end_col
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input. Try again.")

    def is_checkmate(self):
        king = self.find_king()
        if king is None:
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is not None and piece.color != king.color:
                    moves = piece.valid_moves(self.board)
                    if (king.row, king.col) in moves:
                        return True
        return False

    def find_king(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is not None and piece.color == self.players[self.current_player_index].color and piece.piece_type == 'P':
                    return piece
        return None

