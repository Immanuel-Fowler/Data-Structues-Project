import pygame
from pygame.locals import *
import sys
import subprocess
from GameLinkedList import Games

bg = pygame.image.load("Assets/background-project.jpeg")


# main menu, snake, blank, another blank
game_states = [True,False,False,False]

right_arrow_img = pygame.image.load('Assets/right_arrow.png')
left_arrow_img = pygame.image.load('Assets/left_arrow.png')

pygame.init()

WIDTH, HEIGHT = 800, 600
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
MENU_TITLE_FONT = pygame.font.Font(None, 80)
MENU_OPTION_FONT = pygame.font.Font(None, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GAME_OPTIONS = ["Game 1", "Game 2", "Game 3"]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Menu')

def display_text(text, font, size, color, x, y):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    return text_surface, text_rect

def game_menu():
    while True:
        screen.fill(BLACK)
        

        screen.blit(bg, (0, 0))

        thumbnail = pygame.image.load(Games.head.data[1])
        thumbnail = pygame.transform.scale(thumbnail, (100, 100))
        screen.blit(thumbnail, (WIDTH//2 - 50, HEIGHT//2 + 105))

        title_text, title_rect = display_text('Game Menu', None, 80, WHITE, WIDTH // 2, HEIGHT // 4)
        screen.blit(title_text, title_rect)

        option_text, option_rect = display_text(Games.head.data[0], None, 40, WHITE, WIDTH // 2, HEIGHT // 2)
        screen.blit(option_text, option_rect)

        '''screen.blit(pygame.image.load('Assets/right_arrow.png'),(WIDTH, HEIGHT // 4))

        screen.blit(pygame.image.load('Assets/left_arrow.png'),(WIDTH, HEIGHT // 4))'''

        # Display arrows for scrolling through games
        left_arrow = pygame.Rect(100, HEIGHT // 2, 50, 50)
        pygame.draw.rect(screen,(255,0,0),left_arrow)
        

        right_arrow = pygame.Rect(WIDTH-100, HEIGHT // 2, 50, 50)
        pygame.draw.rect(screen,(0,0,255),right_arrow)
        

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if left_arrow.collidepoint(mouse_pos):
                    if Games.head.prev is not None:
                        Games.head = Games.head.prev
                    else:
                        Games.head = Games.tail

                elif right_arrow.collidepoint(mouse_pos):
                    if Games.head.next is not None:
                        Games.head = Games.head.next
                    else:
                        for i in range(Games.node_count-1):
                            Games.head = Games.head.prev
                elif option_rect.collidepoint(mouse_pos):
                    subprocess.call("python3 " + Games.head.data[2], shell=True)



# Main menu loop
def main():
    while True:
        game_menu()
    
if __name__ == "__main__":
    main()

