# Import and initialize the pygame library
import pygame
import random
import math

from pygame import mixer

pygame.init()

# RGB - Red, Green, Blue
white = (255, 255, 255)

# Set up the drawing window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Elor's First game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6
# Using for loop to enter value, other option is
# to enter to the array manual values (different)
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(30)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('caramelSweets.ttf', 32)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('caramelSweets.ttf', 64)

# Play again
play_again_font = pygame.font.Font('caramelSweets.ttf', 32)


def button_play_again():
    play_again_text = play_again_font.render("Play Again", True, white)
    screen.blit(play_again_text, (300, 400))


def game_over_text():
    over_text = over_font.render("Game Over :(", True, white)
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, white)
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x - 16, y - 10))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    # if the distance under 27 pixels
    if distance < 27:
        return True
    else:
        return False


# Run until the user asks to quit
running = True
while running:

    screen.fill(white)
    screen.blit(background, (0, 0))
    # Get mouse coordinates
    mouse = pygame.mouse.get_pos()

    # Events by keyboard clicks
    for event in pygame.event.get():
        # Did the user click the window close button?
        if event.type == pygame.QUIT:
            running = False

        # Keyboard press and release
        if event.type == pygame.KEYDOWN:
            # Key down + Right
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            # Key down + Left
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            # Key down + up
            if event.key == pygame.K_UP:
                playerY_change = -4
            # Key down + down
            if event.key == pygame.K_DOWN:
                playerY_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            # Any key up (right or left or up or down)
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or
                    event.key == pygame.K_DOWN or event.key == pygame.K_UP):
                playerX_change = 0
                playerY_change = 0

    # Check if player not out of range screen
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemy Movement
    for i in range(num_of_enemy):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 1000
            game_over_text()
            button_play_again()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Hitting the target
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        # Call function enemy to show him
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY == 0:
        bullet_state = "ready"
        bulletY = 480

    # Call the player function to show him
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

# Done! Time to quit.
pygame.quit()
