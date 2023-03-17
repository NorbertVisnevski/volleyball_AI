import pygame

from controls.game_environment import GameEnvironment
from controls.keyboard import KeyboardControls
from resources import global_variables


def normal_game():
    controllers = [KeyboardControls(i) for i in range(1, 5)]
    game = GameEnvironment()
    while True:
        game.step()
        game.actions = [control.get_action(None) for control in controllers]
        game.draw()
        game.draw_debug()
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    game.ball.throw_ball(global_variables.active_team)