import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up game constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (67, 125, 56)

# Node class for linked list
class Node:
    def __init__(self, position):
        self.position = position
        self.next = None

# Snake class using a linked list
class Snake:
    def __init__(self):
        self.length = 1
        self.head = Node(((WIDTH // 2), (HEIGHT // 2)))
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = RED

    def get_head_position(self):
        return self.head.position

    def update(self):
        current = self.get_head_position()
        x, y = self.direction
        new = (((current[0] + (x * GRID_SIZE)) % WIDTH), (current[1] + (y * GRID_SIZE)) % HEIGHT)
        new_head = Node(new)
        new_head.next = self.head
        self.head = new_head

        if len(self) > self.length:
            current_node = self.head
            while current_node.next.next:
                current_node = current_node.next
            current_node.next = None

    def reset(self):
        self.length = 1
        self.head = Node(((WIDTH // 2), (HEIGHT // 2)))
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        current_node = self.head
        while current_node:
            pygame.draw.rect(surface, self.color, (current_node.position[0], current_node.position[1], GRID_SIZE, GRID_SIZE))
            current_node = current_node.next

    def __len__(self):
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
        return count

    def hit_wall(self):
        x, y = self.get_head_position()
        return 580 <= x <= 600 or 0 == x <= 1 or 380 <= y <= 400 or 0 == y <= 1

    def hit_self(self):
        current_node = self.head.next
        while current_node:
            if self.get_head_position() == current_node.position:
                return True
            current_node = current_node.next
        return False

# Game loop functions
def draw_grid(surface):
    surface.fill(GREEN)
    # Draw green checkerboard background
    for row in range(0, HEIGHT, GRID_SIZE):
        for col in range(0, WIDTH, GRID_SIZE):
            if (row // GRID_SIZE + col // GRID_SIZE) % 2 == 0:
                pygame.draw.rect(surface, (100, 128, 0), (col, row, GRID_SIZE, GRID_SIZE))
    # Draw one-tile black perimeter
    pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, GRID_SIZE))
    pygame.draw.rect(surface, BLACK, (0, HEIGHT - GRID_SIZE, WIDTH, GRID_SIZE))
    pygame.draw.rect(surface, BLACK, (0, 0, GRID_SIZE, HEIGHT))
    pygame.draw.rect(surface, BLACK, (WIDTH - GRID_SIZE, 0, GRID_SIZE, HEIGHT))

def check_collision(snake, fruit):
    return snake.get_head_position() == fruit

def run_game():

    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    snake = Snake()
    fruit = generate_fruit_position()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.direction = RIGHT

        snake.update()

        if check_collision(snake, fruit):
            snake.length += 1
            fruit = generate_fruit_position()

        if snake.hit_self() or snake.hit_wall():
            print("Game Over! Your score:", snake.length - 1)
            pygame.quit()
            sys.exit()

        draw_grid(surface)
        snake.render(surface)
        pygame.draw.rect(surface, WHITE, (*fruit, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

def generate_fruit_position():
    # Generate a random position for the fruit that avoids the black border
    x = random.randint(4, (WIDTH // GRID_SIZE) - 4) * GRID_SIZE
    y = random.randint(4, (HEIGHT // GRID_SIZE) - 4) * GRID_SIZE
    print(x, y)
    return x, y

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

if __name__ == "__main__":
    run_game()
