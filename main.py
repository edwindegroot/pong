# Example file showing a circle moving on screen
import math
import random

import pygame

# pygame setup
pygame.init()
height = 720
width = 1280
paddle_size = 80
paddle_bottom = height / 2 - paddle_size / 2
paddle_bottom_2 = height / 2 - paddle_size / 2
screen = pygame.display.set_mode((width, height))
offset = 45
paddle_speed = 900
clock = pygame.time.Clock()
running = True
dt = 0
ball_radius = 10
ball_speed = 1200
paddle_width = 15
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
going_right = True
going_down = True
going_up = False
angle = random.uniform(-math.pi / 12, math.pi / 12) + random.randint(0, 1) * math.pi
while angle == 0:
    angle = random.uniform(-math.pi / 12, math.pi / 12) + random.randint(0, 1) * math.pi
score = 0
best_score = 0
score_font = pygame.font.SysFont("monospace", 16)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "red", ball_pos, ball_radius)
    paddle_top = paddle_bottom + paddle_size
    paddle_top_2 = paddle_bottom_2 + paddle_size
    bottom = pygame.Vector2(offset, paddle_bottom)
    bottom_2 = pygame.Vector2(width - offset, paddle_bottom_2)
    top = pygame.Vector2(offset, paddle_top)
    top_2 = pygame.Vector2(width - offset, paddle_top_2)
    pygame.draw.line(screen, 'yellow', bottom, top, paddle_width)
    pygame.draw.line(screen, 'yellow', bottom_2, top_2, paddle_width)

    keys = pygame.key.get_pressed()
    difference = paddle_speed * dt
    if keys[pygame.K_w]:
        if paddle_bottom >= difference:
            paddle_bottom -= difference
    if keys[pygame.K_s]:
        if paddle_bottom + paddle_size + difference <= height:
            paddle_bottom += difference

    if keys[pygame.K_UP]:
        if paddle_bottom_2 >= difference:
            paddle_bottom_2 -= difference
    if keys[pygame.K_DOWN]:
        if paddle_bottom_2 + paddle_size + difference <= height:
            paddle_bottom_2 += difference

    ball_difference = ball_speed * dt
    # if ball_pos.x + ball_radius >= width:
    #     angle = math.pi - angle
    #     going_right = False
    #     going_down = not going_down
    #     going_up = not going_up
    if ball_pos.y + ball_radius >= height:
        angle = - angle
        going_up = False
        going_down = True
    if ball_pos.y + ball_radius <= 0:
        angle = 2 * math.pi - angle
        going_up = True
        going_down = False
    if paddle_bottom - ball_radius <= ball_pos.y <= paddle_top + ball_radius and bottom.x - paddle_width / 2 <= ball_pos.x <= bottom.x + paddle_width / 2:
        score += 1
        angle = math.pi - angle
        going_right = True
        going_down = not going_down
        going_up = not going_up
    if paddle_bottom_2 - ball_radius <= ball_pos.y <= paddle_top_2 + ball_radius and bottom_2.x - paddle_width / 2 <= ball_pos.x <= bottom_2.x + paddle_width / 2:
        score += 1
        angle = math.pi - angle
        going_right = True
        going_down = not going_down
        going_up = not going_up
    if ball_pos.x < 0 or ball_pos.x > width:
        if score > best_score:
            best_score = score
        score = 0
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        paddle_bottom = height / 2 - paddle_size / 2
        angle = random.uniform(-math.pi / 12, math.pi / 12) + random.randint(0, 1) * math.pi
        while angle == 0:
            print(random.randint(0, 2))
            angle = random.uniform(-math.pi / 12, math.pi / 12) + random.randint(0, 1) * math.pi

    ball_pos.x += ball_difference * math.cos(angle)
    ball_pos.y += ball_difference * math.sin(angle)

    if best_score > 0:
        score_text = score_font.render("Score = " + str(score) + ", best = " + str(best_score), 0, 'green')
    else:
        score_text = score_font.render("Score = " + str(score), 0, 'green')
    screen.blit(score_text, (width / 2 - 60, height - 20))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()