import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 50

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Hornet')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)
small_font = pygame.font.SysFont('Bauhaus 93', 30)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
high_score = 0
pass_pipe = False

# load images
bg = pygame.image.load('Games/FlappyHornet/bg.png')
ground_img = pygame.image.load('Games/FlappyHornet/ground.png')
button_img = pygame.image.load('Games/FlappyHornet/restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'Games/FlappyHornet/hornet{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            # jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.clicked:
                self.clicked = True
                self.vel = -10
            if not keys[pygame.K_SPACE]:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Games/FlappyHornet/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


# Linked List Implementation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def remove_node(self, data):
        current = self.head
        if current and current.data == data:
            self.head = current.next
            return
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    def traverse(self):
        current = self.head
        while current:
            # Process current node
            if not game_over:  # Only update if the game is not over
                current.data.update()  # Assuming data in the node is an object with an update method
            if current.data.rect.right < 0:  # Remove pipes that have gone off the screen
                pipe_group.remove(current.data)
                self.remove_node(current.data)
            current = current.next


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

# Create a linked list for pipes
pipes_list = LinkedList()

run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_scroll, 768))

    # Update and draw pipes using linked list
    pipes_list.traverse()

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    if (score >= high_score):
        high_score = score

    draw_text(str('Score'), small_font, white, int(screen_width /2-15), 5)
    draw_text(str(score), font, white, int(screen_width / 2), 30)
    draw_text(str('High Score'), small_font, white, int(screen_width - 110), 5)
    draw_text(str(high_score), font, white, int(screen_width - 70), 30)


    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            pipes_list.add_node(btm_pipe)
            pipes_list.add_node(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()

