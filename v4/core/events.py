import pygame


class EventManager:
    def __init__(self) -> None:
        self.quit = False
        self.mouse_pos = (0, 0)
        self.mouse_down = False

    def process(self):
        self.quit = False
        self.mouse_down = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.type == 1:
                self.mouse_down = True

        self.mouse_pos = pygame.mouse.get_pos()
