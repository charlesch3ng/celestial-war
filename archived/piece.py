class Piece:
    def __init__(self, piece_type, row, col):
        self.piece_type = piece_type
        self.row = row
        self.col = col

    def __str__(self):
        return self.piece_type

    def valid_moves(self, board):
        moves = []
        if self.piece_type == 'P':
            # Planet moves one square in any direction
            for row_offset in [-1, 0, 1]:
                for col_offset in [-1, 0, 1]:
                    if row_offset == 0 and col_offset == 0:
                        continue  # ignore current position
                    new_row = self.row + row_offset
                    new_col = self.col + col_offset
                    if board.is_valid(new_row, new_col) and (board.get_piece(new_row, new_col) is None or board.get_piece(new_row, new_col).piece_type != 'P'):
                        moves.append((new_row, new_col))
        elif self.piece_type == 'M':
            # Moon moves any number of squares diagonally, horizontally, or vertically
            for row_offset in [-1, 0, 1]:
                for col_offset in [-1, 0, 1]:
                    if row_offset == 0 and col_offset == 0:
                        continue  # ignore current position
                    new_row = self.row
                    new_col = self.col
                    while True:
                        new_row += row_offset
                        new_col += col_offset
                        if not board.is_valid(new_row, new_col):
                            break  # stop if new position is out of bounds
                        if board.get_piece(new_row, new_col) is None:
                            moves.append((new_row, new_col))
                        elif board.get_piece(new_row, new_col).piece_type != 'M':
                            moves.append((new_row, new_col))
                            break  # stop if new position is occupied by a different piece type
                        else:
                            break  # stop if new position is occupied by the same piece type
        elif self.piece_type == 'S':
            # Star moves one square diagonally or one or two squares orthogonally
            for row_offset in [-2, -1, 0, 1, 2]:
                for col_offset in [-2, -1, 0, 1, 2]:
                    if row_offset == 0 and col_offset == 0:
                        continue  # ignore current position
                    if abs(row_offset) == abs(col_offset):
                        if board.is_valid(self.row+row_offset, self.col+col_offset) and (board.get_piece(self.row+row_offset, self.col+col_offset) is None or board.get_piece(self.row+row_offset, self.col+col_offset).piece_type != 'S'):
                            moves.append((self.row+row_offset, self.col+col_offset))
                    elif abs(row_offset) + abs(col_offset) in [1, 2]:
                        if board.is_valid(self.row+row_offset, self.col+col_offset) and (board.get_piece(self.row+row_offset, self.col+col_offset) is None or board.get_piece(self.row+row_offset, self.col+col_offset).piece_type != 'S'):
                            moves.append((self.row+row_offset, self.col+col_offset))
        elif self.piece_type == 'C':
            # Comet moves any number of squares diagonally or vertically, but cannot jump over other pieces
            for row_offset in [-1, 0, 1]:
                for col_offset in [-1, 0, 1]:
                    if row_offset == 0 and col_offset == 0:
                        continue  # ignore current position
                    new_row = self.row
                    new_col = self.col
                    while True:
                        new_row += row_offset
                        new_col += col_offset
                        if not board.is_valid(new_row, new_col):
                            break  # stop if new position is out of bounds
                        if board.get_piece(new_row, new_col) is None:
                            moves.append((new_row, new_col))
                        elif board.get_piece(new_row, new_col).piece_type != 'C':
                            moves.append((new_row, new_col))
                            break  # stop if new position is occupied by a different piece type
                        else:
                            break  # stop if new position is occupied by the same piece type
        elif self.piece_type == 'N':
            # Nebula moves one square diagonally or one or two squares horizontally or vertically, but cannot capture
            for row_offset in [-2, -1, 0, 1, 2]:
                for col_offset in [-2, -1, 0, 1, 2]:
                    if row_offset == 0 and col_offset == 0:
                        continue  # ignore current position
                    if abs(row_offset) in [1, 2] and abs(col_offset) in [1, 2]:
                        if board.is_valid(self.row+row_offset, self.col+col_offset) and board.get_piece(self.row+row_offset, self.col+col_offset) is None:
                            moves.append((self.row+row_offset, self.col+col_offset))
                    elif abs(row_offset) in [1, 2] and abs(col_offset) == 0:
                        if board.is_valid(self.row+row_offset, self.col+col_offset) and board.get_piece(self.row+row_offset, self.col+col_offset) is None:
                            moves.append((self.row+row_offset, self.col+col_offset))
                    elif abs(row_offset) == 0 and abs(col_offset) in [1, 2]:
                        if board.is_valid(self.row+row_offset, self.col+col_offset) and board.get_piece(self.row+row_offset, self.col+col_offset) is None:
                            moves.append((self.row+row_offset, self.col+col_offset))
        elif self.piece_type == 'A':
            # Asteroid moves one or two squares diagonally, and captures by jumping over a piece adjacent to it
            for row_offset in [-2, -1, 1, 2]:
                for col_offset in [-2, -1, 1, 2]:
                    if abs(row_offset) == abs(col_offset):
                        continue  # ignore diagonals of more than 2 squares
                    new_row = self.row + row_offset
                    new_col = self.col + col_offset
                    if not board.is_valid(new_row, new_col):
                        continue  # ignore out-of-bounds squares
                    if board.get_piece(new_row, new_col) is None:
                        moves.append((new_row, new_col))
                    else:
                        jump_row = self.row + (row_offset // 2)
                        jump_col = self.col + (col_offset // 2)
                        if board.is_valid(jump_row, jump_col) and board.get_piece(jump_row, jump_col) is not None and board.get_piece(jump_row, jump_col).piece_type != 'A':
                            moves.append((new_row, new_col))
        return moves