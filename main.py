# Project:    2048 Clone
# Author:     Marian Minar
# Date:       June 14, 2023

import pygame
import sys
import random

from pygame.locals import QUIT

# Constants
FPS = 60
GRID_SIZE = 4
GRID_WIDTH = 400
GRID_HEIGHT = 400
CELL_SIZE = 100
CELL_PADDING = 6

# window size should include grid size and cell padding
WINDOW_WIDTH = GRID_WIDTH + (GRID_SIZE + 1) * CELL_PADDING
WINDOW_HEIGHT = GRID_HEIGHT + (GRID_SIZE + 1) * CELL_PADDING

# colors and fonts
BACKGROUND_COLOR = (70, 70, 70)
CELL_COLOR = (255, 255, 255)
TEXT_COLOR = (60, 60, 60)
SCORE_COLOR = (255, 255, 255)
SCORE_FONT_SIZE = 20

# Colors for each tile
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Text for each tile
TEXT = {
    0: "",
    2: "2",
    4: "4",
    8: "8",
    16: "16",
    32: "32",
    64: "64",
    128: "128",
    256: "256",
    512: "512",
    1024: "1024",
    2048: "2048",
}

# Directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

# pygame key events and directions mapping
KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Initialize pygame
running = True
pygame.init()

# Set up the window
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

# Set up the clock
clock = pygame.time.Clock()

# Set up the window title
pygame.display.set_caption("2048")


def draw_cell(window_surface, i, j, cell_color, cell_text):
    # Calculate the cell's position
    x = CELL_PADDING + j * (CELL_SIZE + CELL_PADDING)
    y = CELL_PADDING + i * (CELL_SIZE + CELL_PADDING)

    # Draw the cell
    pygame.draw.rect(window_surface, cell_color, (x, y, CELL_SIZE, CELL_SIZE))

    # Draw the cell's text
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(cell_text, True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (x + CELL_SIZE / 2, y + CELL_SIZE / 2)
    window_surface.blit(text, text_rect)


# draw the board to test
def draw_board(window_surface, board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            draw_cell(window_surface, i, j, COLORS[board[i][j]], TEXT[board[i][j]])


# function to mirror the board horizontally or vertically
def mirror_board(board, direction):
    if direction == LEFT or direction == RIGHT:
        return [row[::-1] for row in board]
    elif direction == UP or direction == DOWN:
        return board[::-1]


# function to rotate the board 90 degrees clockwise or counter-clockwise
def rotate_board(board, direction):
    if direction == UP:  # counter-clockwise
        return [list(row) for row in zip(*board)][::-1]
    elif direction == DOWN:  # clockwise
        return [list(row) for row in zip(*board[::-1])]


# shift the board left (used in shift_board function)
def shift_left(board):
    success = False
    for i in range(GRID_SIZE):
        # Remove all zeros
        row = [x for x in board[i] if x != 0]

        # Add zeros to the end
        while len(row) < GRID_SIZE:
            row.append(0)

        # Merge tiles of the same value
        for j in range(GRID_SIZE - 1):
            if row[j] == row[j + 1]:
                row[j] *= 2
                row[j + 1] = 0

        # Remove all zeros
        row = [x for x in row if x != 0]

        # Add zeros to the end
        while len(row) < GRID_SIZE:
            row.append(0)

        # Update the board
        board[i] = row

        # The board changed
        success = True
    return (board, success)


# shift the board in any direction, but transforming it
# in the appropriate way first and then transforming it back
def shift_board(board, direction, spawn=True):
    success = False

    # Transform the board
    if direction == LEFT:
        board, success = shift_left(board)
        if spawn:
            board, _ = spawn_on_right(board)
    elif direction == RIGHT:
        board = mirror_board(board, RIGHT)
        board, success = shift_left(board)
        if spawn:
            board, _ = spawn_on_right(board)
        board = mirror_board(board, LEFT)
    elif direction == UP:
        board = rotate_board(board, UP)
        board, success = shift_left(board)
        if spawn:
            board, _ = spawn_on_right(board)
        board = rotate_board(board, DOWN)
    elif direction == DOWN:
        board = rotate_board(board, DOWN)
        board, success = shift_left(board)
        if spawn:
            board, _ = spawn_on_right(board)
        board = rotate_board(board, UP)

    return (board, success)


# function to spawn a new tile after a horizontal shift
# Spawn a new tile in the corresponding column, in a random row.
# The tile's value is randomly 2 or 4.
def spawn_on_right(board):
    success = False
    # get the index of a random empty cell in the last column
    empty_cells = []
    for i in range(GRID_SIZE):
        if board[i][GRID_SIZE - 1] == 0:
            empty_cells.append(i)
    if len(empty_cells) > 0:
        # randomly select one of the empty cells
        i = random.choice(empty_cells)
        # set it's value to 2 or 4
        board[i][GRID_SIZE - 1] = random.choice([2, 4])
        success = True

    return (board, success)


# a function that returns a random starting board
# the starting board should have at least 2 tiles
def random_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if random.random() < 0.15:
                board[i][j] = 2
    # check to see if the board is empty
    if sum([sum(row) for row in board]) == 0:
        return random_board()
    else:
        return board


# Main game loop
def main(board=random_board()):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # if the left key is pressed, shift the board left
            if event.type == pygame.KEYDOWN:
                if event.key in (
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                ):
                    board, _ = shift_board(board, KEY_TO_DIRECTION[event.key])

        # Draw the background
        window_surface.fill(BACKGROUND_COLOR)

        # Draw the board
        draw_board(window_surface, board)

        # Draw the window onto the screen
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

# NOTE: not yet implemented
# Create some tests
# test_board = [
#     [0, 0, 0, 2],
#     [0, 4, 0, 2],
#     [0, 0, 8, 0],
#     [0, 0, 0, 2],
# ]
# assert shift_board(test_board, LEFT, False) == (
#     [[2, 0, 0, 0], [4, 2, 0, 0], [8, 0, 0, 0], [2, 0, 0, 0]],
#     True,
# )
# assert shift_board(test_board, RIGHT, False) == (
#     [[0, 0, 0, 2], [0, 0, 4, 2], [0, 0, 0, 8], [0, 0, 0, 2]],
#     True,
# )
# assert shift_board(test_board, UP, False) == (
#     [[0, 4, 8, 2], [0, 0, 8, 0], [0, 0, 0, 2], [0, 0, 0, 0]],
#     True,
# )
# assert shift_board(test_board, DOWN, False) == (
#     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2], [0, 4, 8, 4]],
#     True,
# )
