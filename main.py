import pygame
from celestial_war import GameBoard


# Initialize pygame
pygame.init()

# Define screen dimensions and colors
WIDTH, HEIGHT = 800, 800
BACKGROUND_COLOR = (30, 30, 30)
GRID_COLOR = (230, 230, 230)
SQUARE_SIZE = WIDTH // 10

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial War")

# Initialize the game board
game_board = GameBoard()

def draw_board():

    for x in range(10):
        for y in range(10):
            piece = game_board.get_piece((x, y))
            if piece:
                piece_type = piece.__class__.__name__.lower()
                piece_color = piece.color.lower()
                image_key = f"{piece_color}_{piece_type}"
                image = piece_images[image_key]
                screen.blit(image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

            rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

            pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def load_piece_images():
    pieces = ["king", "queen", "star", "comet", "nebula", "asteroid"]
    colors = ["white", "black"]
    images = {}

    for color in colors:
        for piece in pieces:
            image_name = f"{color}_{piece}.png"
            image = pygame.image.load(f"images/{image_name}")
            scaled_image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
            images[f"{color}_{piece}"] = scaled_image
    return images


piece_images = load_piece_images()


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    draw_board()

    pygame.display.flip()

pygame.quit()