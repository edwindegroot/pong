# Example file showing a circle moving on screen
import math
import random

import pygame


class Game:
    pygame.init()
    height = 720
    width = 1280
    paddle_size = 80
    paddle_1_bottom = height / 2 - paddle_size / 2
    paddle_2_bottom = height / 2 - paddle_size / 2
    screen = pygame.display.set_mode((width, height))
    offset = 45
    paddle_speed = 900
    clock = pygame.time.Clock()
    running = True
    dt = 0
    ball_radius = 10
    ball_speed = 700
    paddle_width = 15
    ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    angle = None
    score_1 = 0
    score_2 = 0
    score_font = pygame.font.SysFont("monospace", 16)

    def init(self):
        self.ball_speed = 800
        angle = random.uniform(-math.pi / 12, math.pi / 12)
        while -math.pi / 18 <= angle <= math.pi / 18:
            angle = random.uniform(-math.pi / 12, math.pi / 12)
        self.angle = angle + random.randint(0, 1) * math.pi

    def quit_on_x(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        difference = self.paddle_speed * self.dt
        if keys[pygame.K_w]:
            if self.paddle_1_bottom >= difference:
                self.paddle_1_bottom -= difference
        if keys[pygame.K_s]:
            if self.paddle_1_bottom + self.paddle_size + difference <= self.height:
                self.paddle_1_bottom += difference

        if keys[pygame.K_UP]:
            if self.paddle_2_bottom >= difference:
                self.paddle_2_bottom -= difference
        if keys[pygame.K_DOWN]:
            if self.paddle_2_bottom + self.paddle_size + difference <= self.height:
                self.paddle_2_bottom += difference

    def draw(self, bottom_1, bottom_2, paddle_top_1, paddle_top_2):
        top_1 = pygame.Vector2(self.offset, paddle_top_1)
        top_2 = pygame.Vector2(self.width - self.offset, paddle_top_2)
        pygame.draw.circle(self.screen, "red", self.ball_pos, self.ball_radius)
        pygame.draw.line(self.screen, 'yellow', bottom_1, top_1, self.paddle_width)
        pygame.draw.line(self.screen, 'yellow', bottom_2, top_2, self.paddle_width)

    def check_ball_borders(self, bottom_1, bottom_2, paddle_top_1, paddle_top_2):
        if self.ball_pos.y + self.ball_radius >= self.height:
            self.angle = - self.angle
        if self.ball_pos.y + self.ball_radius <= 0:
            self.angle = 2 * math.pi - self.angle
        if (self.paddle_1_bottom - self.ball_radius <= self.ball_pos.y <= paddle_top_1 + self.ball_radius and bottom_1.x
                - self.paddle_width / 2 <= self.ball_pos.x <= bottom_1.x + self.paddle_width / 2):
            self.ball_speed = 1200
            self.angle = math.pi - self.angle
        if (self.paddle_2_bottom - self.ball_radius <= self.ball_pos.y <= paddle_top_2 + self.ball_radius and bottom_2.x
                - self.paddle_width / 2 <= self.ball_pos.x <= bottom_2.x + self.paddle_width / 2):
            self.ball_speed = 1200
            self.angle = math.pi - self.angle
        if self.ball_pos.x < 0 or self.ball_pos.x > self.width:
            if self.ball_pos.x < 0:
                self.score_2 += 1
            else:
                self.score_1 += 1
            self.ball_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
            self.paddle_1_bottom = self.height / 2 - self.paddle_size / 2
            self.init()

    def show_score(self):
        score_text_1 = self.score_font.render("Score = " + str(self.score_1), 0, 'green')
        score_text_2 = self.score_font.render("Score = " + str(self.score_2), 0, 'green')
        self.screen.blit(score_text_1, (self.width / 4 - 60, self.height - 20))
        self.screen.blit(score_text_2, ((self.width / 4) * 3 - 60, self.height - 20))

    def boilerplate_flip_and_fps(self):
        pygame.display.flip()
        self.dt = self.clock.tick(60) / 1000

    def run(self):
        while self.running:
            self.quit_on_x()

            self.screen.fill("black")

            self.handle_input()
            bottom_1 = pygame.Vector2(self.offset, self.paddle_1_bottom)
            bottom_2 = pygame.Vector2(self.width - self.offset, self.paddle_2_bottom)
            paddle_top_1 = self.paddle_1_bottom + self.paddle_size
            paddle_top_2 = self.paddle_2_bottom + self.paddle_size
            self.draw(bottom_1, bottom_2, paddle_top_1, paddle_top_2)

            ball_difference = self.ball_speed * self.dt
            self.ball_pos.x += ball_difference * math.cos(self.angle)
            self.ball_pos.y += ball_difference * math.sin(self.angle)
            self.check_ball_borders(bottom_1, bottom_2, paddle_top_1, paddle_top_2)
            self.show_score()
            self.boilerplate_flip_and_fps()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.init()
    game.run()
