import sys

import pygame.sprite

import layer
import assets
import configs



# создание окна завершения игры
class GameOver(pygame.sprite.Sprite):
    # инициализация окна
    def __init__(self, *groups):
        self._layer = layer.Layer.INTERFACE
        self.image = assets.get_sprite('gameover')
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2 - 69))

        self.button_reset = pygame.image.load('assets/sprites/reset_end.png')
        self.button_exit = pygame.image.load('assets/sprites/exit_end.png')

        self.button_reset_rect = self.button_reset.get_rect(center=(configs.SCREEN_WIDTH / 2,
                                                                    configs.SCREEN_HEIGHT - 210))
        self.button_exit_rect = self.button_exit.get_rect(center=(configs.SCREEN_WIDTH / 2,
                                                                  configs.SCREEN_HEIGHT - 140))

        super().__init__(*groups)

    # отрисовка кнопок после проигрыша
    def draw_buttons(self, screen):
        screen.blit(self.button_reset, self.button_reset_rect.topleft)
        screen.blit(self.button_exit, self.button_exit_rect.topleft)

    # смотриим положение мышки при нажатии на нее
    def handle_event(self, event, n):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.button_reset_rect.collidepoint(mouse_pos):
                return True
            elif self.button_exit_rect.collidepoint(mouse_pos):
                assets.write(str(n))
                assets.record()
                print(assets.record)
                self.exit_game()

    # выход из игры
    def exit_game(self):
        pygame.quit()
        sys.exit()
