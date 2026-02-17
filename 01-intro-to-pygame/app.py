import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Game state
score = 0
auto_increment = 1
click_bonus = 10
timer = 0.0
increment_interval = 1.0  # seconds

running = True
while running:
    dt = clock.tick(60) / 1000.0  # delta time in seconds

    # 1. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            score += click_bonus

    # 2. Update
    timer += dt
    if timer >= increment_interval:
        score += auto_increment
        timer = 0.0

    # 3. Draw
    screen.fill((30, 30, 30))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    hint_text = font.render("Click to earn bonus points!", True, (180, 180, 180))

    screen.blit(score_text, (300, 250))
    screen.blit(hint_text, (220, 320))

    pygame.display.flip()

pygame.quit()
sys.exit()
