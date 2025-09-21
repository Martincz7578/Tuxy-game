import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
GRAVITY = 0.25
JUMP = -6.5
PIPE_GAP = 150
PIPE_FREQ = 1500

bg_img = pygame.image.load('imgs/background.jpg').convert()
ground_img = pygame.image.load('imgs/win98.png').convert_alpha()
tuxy_img = pygame.image.load('imgs/tux.png').convert_alpha()
pipe_img = pygame.image.load('imgs/pipe.png').convert_alpha()

bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
ground_img = pygame.transform.scale(ground_img, (WIDTH, 100))
tuxy_img = pygame.transform.scale(tuxy_img, (50, 35))
pipe_img = pygame.transform.scale(pipe_img, (80, 500))

font = pygame.font.SysFont('Arial', 40)

def draw_text(text, x, y):
    img = font.render(text, True, (255,255,255))
    SCREEN.blit(img, (x, y))

class Tuxy:
    def __init__(self):
        self.x = 60
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = tuxy_img.get_rect(center=(self.x, self.y))
    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.centery = self.y
    def jump(self):
        self.vel = JUMP
    def draw(self):
        SCREEN.blit(tuxy_img, self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT-PIPE_GAP-200)
        self.top_rect = pipe_img.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = pipe_img.get_rect(midtop=(self.x, self.height+PIPE_GAP))
    def update(self):
        self.x -= 3
        self.top_rect.centerx = self.x
        self.bottom_rect.centerx = self.x
    def draw(self):
        SCREEN.blit(pipe_img, self.top_rect)
        SCREEN.blit(pygame.transform.flip(pipe_img, False, True), self.bottom_rect)
    def off_screen(self):
        return self.x < -80
    def collide(self, tuxy_rect):
        return self.top_rect.colliderect(tuxy_rect) or self.bottom_rect.colliderect(tuxy_rect)

def main():
    tuxy = Tuxy()
    pipes = []
    ground_x = 0
    score = 0
    last_pipe = pygame.time.get_ticks()
    running = True
    game_over = False
    while running:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    tuxy.jump()
                if event.key == pygame.K_SPACE and game_over:
                    main()
        SCREEN.blit(bg_img, (0,0))
        if not game_over:
            tuxy.update()
            now = pygame.time.get_ticks()
            if now - last_pipe > PIPE_FREQ:
                pipes.append(Pipe(WIDTH+40))
                last_pipe = now
            for pipe in pipes:
                pipe.update()
                pipe.draw()
            pipes = [p for p in pipes if not p.off_screen()]
            for pipe in pipes:
                if pipe.collide(tuxy.rect):
                    game_over = True
            if pipes and pipes[0].x + 40 < tuxy.x and not hasattr(pipes[0], 'scored'):
                score += 1
                pipes[0].scored = True
            if tuxy.y > HEIGHT-100 or tuxy.y < 0:
                game_over = True
        tuxy.draw()
        ground_x = (ground_x - 3) % WIDTH
        SCREEN.blit(ground_img, (ground_x, HEIGHT-100))
        SCREEN.blit(ground_img, (ground_x-WIDTH, HEIGHT-100))
        draw_text(str(score), WIDTH//2-20, 30)
        if game_over:
            draw_text('Game Over', WIDTH//2-100, HEIGHT//2-40)
            draw_text('Press SPACE', WIDTH//2-110, HEIGHT//2+10)
        pygame.display.flip()

if __name__ == '__main__':
    main()