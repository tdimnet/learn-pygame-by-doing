import sys
import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

