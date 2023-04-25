class GameBoard:
    def __init__(self):
        self.board = [[None for _ in range(10)] for _ in range(10)]

        for i in range(10):
            self.board[1][i] = Asteroid((i, 1), "black")
            self.board[8][i] = Asteroid((i, 8), "white")

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
            self.board[0][index] = piece_class((index, 0), "black")
            self.board[9][index] = piece_class((index, 9), "white")

    def move_piece(self, piece, new_position):
        if not piece.is_valid_move(new_position, self):
            raise ValueError("Invalid move")

        target_piece = self.get_piece(new_position)

        if isinstance(piece, Asteroid) and target_piece is None:
            capture_x = (new_position[0] + piece.position[0]) // 2
            capture_y = (new_position[1] + piece.position[1]) // 2
            capture_position = (capture_x, capture_y)
            target_piece = self.get_piece(capture_position)
            self.board[capture_y][capture_x] = None

        self.board[piece.position[1]][piece.position[0]] = None
        self.board[new_position[1]][new_position[0]] = piece
        piece.position = new_position

        return target_piece

    def capture_piece(self, piece, new_position):
        target_piece = self.board[new_position[1]][new_position[0]]
        if target_piece and target_piece.color != piece.color:
            return target_piece
        return None

    def is_empty_square(self, position):
        return self.board[position[1]][position[0]] is None

    def get_piece(self, position):
        return self.board[position[1]][position[0]]


class Piece:
    def __init__(self, position, color):
        self.position = position
        self.color = color

class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
    def is_valid_move(self, new_position, game_board):
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])
        return dx <= 1 and dy <= 1

class Queen(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
    def is_valid_move(self, new_position, game_board):
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])
        return dx == dy or dx == 0 or dy == 0

class Star(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
    def is_valid_move(self, new_position, game_board):
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])

        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1) or (dx == 2 and dy == 0) or (dx == 0 and dy == 2) or (dx == 1 and dy == 1):
            target_piece = game_board.get_piece(new_position)
            return not target_piece or target_piece.color != self.color

        return False


class Comet(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
    def is_valid_move(self, new_position, game_board):
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])

        if (dx == 0 and dy > 0) or (dy == dx > 0):
            step_x = 1 if new_position[0] > self.position[0] else -1
            step_y = 1 if new_position[1] > self.position[1] else -1

            x, y = self.position
            x += step_x
            y += step_y

            while x != new_position[0] and y != new_position[1]:
                if not game_board.is_empty_square((x, y)):
                    return False
                x += step_x
                y += step_y

            target_piece = game_board.get_piece(new_position)
            return not target_piece or target_piece.color != self.color

        return False


class Nebula(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
    def is_valid_move(self, new_position, game_board):
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])
        return (dx <= 2 and dy == 0) or (dx == 0 and dy <= 2) or (dx == dy and dx == 1)

class Asteroid(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
    def is_valid_move(self, new_position, game_board):
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])

        if dx == 2 and dy == 2:
            capture_x = (new_position[0] + self.position[0]) // 2
            capture_y = (new_position[1] + self.position[1]) // 2
            capture_position = (capture_x, capture_y)
            captured_piece = game_board.board[capture_y][capture_x]

            if captured_piece and captured_piece.color != self.color:
                return True

        return False
