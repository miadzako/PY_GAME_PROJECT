import pygame.sprite

import assets
import configs
import layer

#функция отвечающая за создания пола
class Floor(pygame.sprite.Sprite):
    def __init__(self, k, *groups):
        self._layer = layer.Layer.FLOOR
        self.image = assets.get_sprite('floor')
        self.rect = self.image.get_rect(bottomleft=(configs.SCREEN_WIDTH * k, configs.SCREEN_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2
        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH

