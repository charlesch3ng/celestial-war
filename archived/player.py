class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.captured_pieces = []

    def __str__(self):
        return self.name

    def capture_piece(self, piece):
        self.captured_pieces.append(piece)