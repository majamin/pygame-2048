# A 2048 game clone

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
    0: (255, 255, 255),
    2: (231, 4, 255),
    4: (219, 6, 255),
    8: (207, 8, 255),
    16: (195, 10, 255),
    32: (183, 12, 255),
    64: (171, 14, 255),
    128: (159, 16, 255),
    256: (147, 18, 255),
    512: (135, 110, 255),
    1024: (123, 121, 255),
    2048: (111, 132, 255),
    4096: (99, 143, 255),
    8192: (87, 154, 255),
    16384: (75, 165, 255),
    32768: (63, 176, 255),
    65536: (51, 187, 255),
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
    4096: "4096",
    8192: "8192",
    16384: "16384",
    32768: "32768",
    65536: "65536",
}

# Directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

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
            draw_cell(window_surface, i, j, CELL_COLOR, TEXT[board[i][j]])


# Shift the board to the left.
# All tiles move as far left as possible.
# Tiles on the same row and value are merged.
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


# Shift the board to the right, use the shift_left function
def shift_right(board):
    success = False
    # mirror the board
    board = [row[::-1] for row in board]
    # shift the board left
    board, success = shift_left(board)
    # mirror it back
    board = [row[::-1] for row in board]
    return (board, success)

# function to spawn a new tile after a horizontal shift
# Spawn a new tile in the corresponding column, in a random row.
# The tile's value is randomly 2 or 4.
def spawn_new(board, direction):
    success = False
    mirrored = False
    # if direction is right, mirror the board
    if direction == RIGHT:
        board = [row[::-1] for row in board]
        mirrored = True

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

    # if direction is right, mirror the board back
    if mirrored:
        board = [row[::-1] for row in board]

    return (board, success)



# Shift the board up.
# All tiles move as far up as possible.
# Tiles in the same column and value are merged.
def shift_up(board):
    for j in range(GRID_SIZE):
        # Remove all zeros
        column = [board[i][j] for i in range(GRID_SIZE) if board[i][j] != 0]

        # Add zeros to the end
        while len(column) < GRID_SIZE:
            column.append(0)

        # Merge tiles of the same value
        for i in range(GRID_SIZE - 1):
            if column[i] == column[i + 1]:
                column[i] *= 2
                column[i + 1] = 0

        # Remove all zeros
        column = [x for x in column if x != 0]

        # Add zeros to the end
        while len(column) < GRID_SIZE:
            column.append(0)

        # Update the board
        for i in range(GRID_SIZE):
            board[i][j] = column[i]


# Shift the board down.
# All tiles move as far down as possible.
# Tiles in the same column and value are merged.
def shift_down(board):
    for j in range(GRID_SIZE):
        # Remove all zeros
        column = [board[i][j] for i in range(GRID_SIZE) if board[i][j] != 0]

        # Add zeros to the beginning
        while len(column) < GRID_SIZE:
            column.insert(0, 0)

        # Merge tiles of the same value
        for i in range(GRID_SIZE - 1, 0, -1):
            if column[i] == column[i - 1]:
                column[i] *= 2
                column[i - 1] = 0

        # Remove all zeros
        column = [x for x in column if x != 0]

        # Add zeros to the beginning
        while len(column) < GRID_SIZE:
            column.insert(0, 0)

        # Update the board
        for i in range(GRID_SIZE):
            board[i][j] = column[i]


# Set up a test game board with random (lower) values
board = [
    [random.choice([0, 0, 0, 2, 4, 8]) for _ in range(GRID_SIZE)]
    for _ in range(GRID_SIZE)
]

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # if the left key is pressed, shift the board left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                board, running = shift_left(board)
                if running:
                    board, running = spawn_new(board, LEFT)
            if event.key == pygame.K_RIGHT:
                board, running = shift_right(board)
                if running:
                    board, running = spawn_new(board, RIGHT)

    # Draw the background
    window_surface.fill(BACKGROUND_COLOR)

    # Draw the board
    draw_board(window_surface, board)

    # Draw the window onto the screen
    pygame.display.update()
    clock.tick(FPS)
