from piece import Piece

class Board:
    def __init__(self):
        self.grid = [[None for col in range(8)] for row in range(8)]
        self.gravity_zones = {
            (0, 0): [(0, 1), (1, 0)],
            (0, 7): [(0, 6), (1, 7)],
            (7, 0): [(7, 1), (6, 0)],
            (7, 7): [(7, 6), (6, 7)],
            (3, 3): [(2, 3), (4, 3), (3, 2), (3, 4)],
            (3, 4): [(2, 4), (4, 4), (3, 3), (3, 5)],
            (4, 3): [(4, 2), (4, 4), (3, 3), (5, 3)],
            (4, 4): [(4, 3), (4, 5), (3, 4), (5, 4)]
        }

    def initiate(self, pieces=None, piece_data=None):
        # Creates and places the starting pieces for the game
        if pieces is None:
            pieces = []

        if piece_data is None:
            piece_data = [
                {'type': 'planet', 'symbol': 'P', 'row': 0, 'col': 4},
                {'type': 'planet', 'symbol': 'P', 'row': 7, 'col': 4},
                {'type': 'moon', 'symbol': 'M', 'row': 0, 'col': 3},
                {'type': 'moon', 'symbol': 'M', 'row': 7, 'col': 3},
                {'type': 'star', 'symbol': 'S', 'row': 0, 'col': 2},
                {'type': 'star', 'symbol': 'S', 'row': 0, 'col': 5},
                {'type': 'star', 'symbol': 'S', 'row': 7, 'col': 2},
                {'type': 'star', 'symbol': 'S', 'row': 7, 'col': 5},
                {'type': 'comet', 'symbol': 'C', 'row': 0, 'col': 1},
                {'type': 'comet', 'symbol': 'C', 'row': 0, 'col': 6},
                {'type': 'comet', 'symbol': 'C', 'row': 7, 'col': 1},
                {'type': 'comet', 'symbol': 'C', 'row': 7, 'col': 6},
                {'type': 'nebula', 'symbol': 'N', 'row': 0, 'col': 0},
                {'type': 'nebula', 'symbol': 'N', 'row': 0, 'col': 7},
                {'type': 'nebula', 'symbol': 'N', 'row': 7, 'col': 0},
                {'type': 'nebula', 'symbol': 'N', 'row': 7, 'col': 7},
            ]

        if len(piece_data) == 0:
            return pieces

        piece_info = piece_data.pop(0)
        piece_type = piece_info['type']
        piece_symbol = piece_info['symbol']
        piece_row = piece_info['row']
        piece_col = piece_info['col']
        piece = Piece(piece_symbol, 'white', piece_type)
        self.set_piece(piece_row, piece_col, piece)
        pieces.append(piece)

        if piece_row != 0:
            piece = Piece(piece_symbol, 'black', piece_type)
            self.set_piece(7 - piece_row, piece_col, piece)
            pieces.append(piece)

        return self.initiate(pieces, piece_data)

    def is_valid(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        return self.grid[row][col]

    def set_piece(self, row, col, piece):
        self.grid[row][col] = piece

    def remove_piece(self, row, col):
        self.grid[row][col] = None

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)
        self.remove_piece(start_row, start_col)
        self.set_piece(piece, end_row, end_col)
        piece.row = end_row
        piece.col = end_col
        if (end_row, end_col) in self.gravity_zones:
            for row, col in self.gravity_zones[(end_row, end_col)]:
                if self.is_valid(row, col) and self.get_piece(row, col) is None:
                    self.move_piece(end_row, end_col, row, col)
                    break

    def __str__(self):
        rows = []
        for i in range(8):
            row = []
            for j in range(8):
                piece = self.get_piece(i, j)
                if piece is None:
                    row.append(".")
                else:
                    row.append(piece.piece_type)
            rows.append(" ".join(row))
        return "\n".join(rows)
