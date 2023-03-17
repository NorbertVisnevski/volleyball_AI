import pygame

header = ['avg', 'min', 'max', 'cumulative', 'table_size', 'epsilon', 'episode']


class GlobalFunctions:

    def __init__(self):
        self.draw = False

    def handle_global_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_TAB]:
                    self.draw = not self.draw
