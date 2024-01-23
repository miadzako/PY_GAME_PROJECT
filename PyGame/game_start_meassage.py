import pygame.sprite
import layer
import assets
import configs

#функция отвечающая за создания окно начала игры
class GameStart(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = layer.Layer.INTERFACE
        self.image = assets.get_sprite('message')
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))

        super().__init__(*groups)
