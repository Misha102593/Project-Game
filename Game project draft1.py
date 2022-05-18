import pygame
import random
from sys import exit

pygame.init()

# images
background_image = 'background.png'
player_character_image = 'player.png'
enemy_character_image = 'enemy.png'
bullet = 'bullet.png'

# Screen info
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load(background_image).convert()
pygame.display.set_caption("Game Project")
screen_display = False

# Bullet info
bullet_image_rep = pygame.image.load(bullet)
bullets_magazine = []
bullet_counter = 0


# Player info

player_image = pygame.image.load(player_character_image)
player_X = 100
player_Y = 300
player_X_change = 0
player_Y_change = 0
player_instance = []

# Enemy info
enemy_image = pygame.image.load(enemy_character_image)
enemy_list = []


# Score
destroy_value = 0


# Classes
class Bullet:

    bullet_speed = 0.5

    def __init__(self, x, y):
        self.bullet_position_X = x
        self.bullet_position_Y = y
        self.bullet_hitbox = 0

        # pygame.draw.rect(self.surface, self.color, pygame.Rect(self.position_X, self.position_Y, 15, 15), 0)

    def fire(self):
        self.bullet_position_X += self.bullet_speed

        self.bullet_hitbox = pygame.Rect(self.bullet_position_X + 32, self.bullet_position_Y + 16, 32, 32)

        screen.blit(bullet_image_rep, (self.bullet_position_X + 32, self.bullet_position_Y + 16))

        pygame.draw.rect(screen, (0, 0, 0), self.bullet_hitbox, 2)


class Enemy:
    def __init__(self):
        self.enemy_position_X = 900
        self.enemy_position_Y = random.randint(50, 520)
        self.enemy_speed = 0.4
        self.enemy_hitbox = 0

    def move(self):
        self.enemy_position_X -= self.enemy_speed
        screen.blit(enemy_image, (self.enemy_position_X, self.enemy_position_Y))
        self.enemy_hitbox = pygame.Rect(self.enemy_position_X, self.enemy_position_Y, 64, 64)
        pygame.draw.rect(screen, (0, 0, 0), self.enemy_hitbox, 2)


class Player:

    def __init__(self, x, y):
        self.player_X = x
        self.player_Y = y
        self.player_hitbox = 0

    def move(self):
        self.player_hitbox = pygame.Rect(player_X, player_Y, 64, 64)
        pygame.draw.rect(screen, (0, 0, 0), self.player_hitbox, 2)
        screen.blit(player_image, (self.player_X, self.player_Y))



# User defined functions


def show_score(x,y):
    score = font.render('Destroyed: ' + str(destroy_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over(x, y, bullets_used, enemies_destroyed):
    display = font_game_over.render("Game Over", True, (255, 255, 255))
    screen.blit(display, (x, y))
    calculated_score = ((enemies_destroyed / bullets_used) * 1000) + enemies_destroyed
    score_board = total_score.render("Score: {:.2f}".format(calculated_score), True, (255, 255, 255))
    screen.blit(score_board, (x, y + 50))


# Main game loop
running = True
while running:

    # Enemy spawner
    enemy_spawn = random.randint(1, 500)

    if enemy_spawn == 10:
        enemy_list.append(Enemy())

    # Font of score-box and game over display
    font = pygame.font.Font('freesansbold.ttf', 32)
    font_game_over = pygame.font.Font('freesansbold.ttf', 50)
    total_score = pygame.font.Font('freesansbold.ttf', 25)

    # Make background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Player movement
        if event.type == pygame.KEYDOWN:  # When key is pressed

            if event.key == pygame.K_LEFT:
                player_X_change = -0.7

            elif event.key == pygame.K_RIGHT:
                player_X_change = 0.7

            elif event.key == pygame.K_UP:
                player_Y_change = -0.7

            elif event.key == pygame.K_DOWN:
                player_Y_change = 0.7

            elif event.key == pygame.K_SPACE:

                bullets_magazine.append(Bullet(player_X, player_Y))
                bullet_counter += 1

        if event.type == pygame.KEYUP:  # When key is released

            if event.key == pygame.K_LEFT:
                player_X_change = 0

            elif event.key == pygame.K_RIGHT:
                player_X_change = 0

            elif event.key == pygame.K_UP:
                player_Y_change = 0

            elif event.key == pygame.K_DOWN:
                player_Y_change = 0

    # Player change of position
    player_X += player_X_change
    player_Y += player_Y_change

    # Display player + hitbox
    player = Player(player_X, player_Y)
    player.move()

    # Bullet/enemy collision
    for enemy in enemy_list:
        enemy.move()
        if enemy.enemy_position_X < -64:
            enemy_list.remove(enemy)
        if enemy.enemy_position_X < 0:
            pass
        if pygame.Rect.colliderect(player.player_hitbox, enemy.enemy_hitbox):
            running = False
            screen_display = True
            break

    for bullet in bullets_magazine:
        bullet.fire()
        for i in enemy_list:
            if pygame.Rect.colliderect(bullet.bullet_hitbox, i.enemy_hitbox):
                bullets_magazine.remove(bullet)
                enemy_list.remove(i)
                destroy_value += 1
        if bullet.bullet_position_X > 800:
            bullets_magazine.remove(bullet)

    # Boundaries
    if player_X <= 0:
        player_X = 0
        if player_Y >= 536:
            player_Y = 536
        elif player_Y <= 0:
            player_Y = 0

    elif player_X >= 736:
        player_X = 736
        if player_Y <= 0:
            player_Y = 0
        elif player_Y >= 536:
            player_Y = 536

    elif player_Y <= 0:
        player_Y = 0

    elif player_Y >= 536:
        player_Y = 536

    show_score(550, 0)

    while screen_display:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0, 0))
        game_over(260, 260, bullet_counter, destroy_value)

        pygame.display.update()

    pygame.display.update()



wasssaaaaa






# set timer/ player gets more points the longer they survive
