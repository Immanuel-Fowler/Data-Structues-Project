import pygame
import random

# Constants
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
BG_COLOR = (187, 173, 160)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 40

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Game grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to add a new tile (either 2 or 4) to a random empty cell
def add_tile():
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

# Function to render the game grid
def render():
    screen.fill(BG_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_color = get_color(grid[i][j])
            pygame.draw.rect(screen, cell_color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, FONT_COLOR)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)
    pygame.display.flip()

# Function to get tile color based on value
def get_color(value):
    colors = {
        0: (205, 192, 180),
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
        2048: (237, 194, 46)
    }
    return colors.get(value, (0, 0, 0))

# Function to move tiles left
def move_left():
    for i in range(GRID_SIZE):
        row = [val for val in grid[i] if val != 0]
        row += [0] * (GRID_SIZE - len(row))
        for j in range(1, GRID_SIZE):
            if row[j] == row[j - 1]:
                row[j - 1] *= 2
                row[j] = 0
        row = [val for val in row if val != 0]
        row += [0] * (GRID_SIZE - len(row))
        grid[i] = row

# Function to move tiles right
def move_right():
    for i in range(GRID_SIZE):
        row = [val for val in grid[i] if val != 0]
        row = [0] * (GRID_SIZE - len(row)) + row
        for j in range(GRID_SIZE - 1, 0, -1):
            if row[j] == row[j - 1]:
                row[j] *= 2
                row[j - 1] = 0
        row = [val for val in row if val != 0]
        row = [0] * (GRID_SIZE - len(row)) + row
        grid[i] = row

# Function to move tiles up
def move_up():
    for j in range(GRID_SIZE):
        col = [grid[i][j] for i in range(GRID_SIZE) if grid[i][j] != 0]
        col += [0] * (GRID_SIZE - len(col))
        for i in range(1, GRID_SIZE):
            if col[i] == col[i - 1]:
                col[i - 1] *= 2
                col[i] = 0
        col = [val for val in col if val != 0]
        col += [0] * (GRID_SIZE - len(col))
        for i in range(GRID_SIZE):
            grid[i][j] = col[i]

# Function to move tiles down
def move_down():
    for j in range(GRID_SIZE):
        col = [grid[i][j] for i in range(GRID_SIZE) if grid[i][j] != 0]
        col = [0] * (GRID_SIZE - len(col)) + col
        for i in range(GRID_SIZE - 1, 0, -1):
            if col[i] == col[i - 1]:
                col[i] *= 2
                col[i - 1] = 0
        col = [val for val in col if val != 0]
        col = [0] * (GRID_SIZE - len(col)) + col
        for i in range(GRID_SIZE):
            grid[i][j] = col[i]

# Function to check if the game is over
def is_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False
    return True

# Initial tiles
add_tile()
add_tile()

# Game loop
running = True
while running:
    render()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not is_game_over():
            if event.key == pygame.K_LEFT:
                move_left()
                add_tile()
            elif event.key == pygame.K_RIGHT:
                move_right()
                add_tile()
            elif event.key == pygame.K_UP:
                move_up()
                add_tile()
            elif event.key == pygame.K_DOWN:
                move_down()
                add_tile

