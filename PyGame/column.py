import random

import pygame.sprite
import assets
import configs
import layer


class Column(pygame.sprite.Sprite):
    def __init__(self, *groups):
        # создаем слой колонн и расстояние между ними
        self._layer = layer.Layer.COLUMN
        self.gap = 100
        # создаем спрайт для колонн
        self.sprite = assets.get_sprite(f'{configs.name_columns}')
        self.sprite_rect = self.sprite.get_rect()
        # прописываем координаты колонн для дальнейшего их создания
        self.pipe_bottom = self.sprite
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(topleft=(0, self.sprite_rect.height + self.gap))

        self.pipe_top = pygame.transform.flip(self.sprite, False, True)
        self.pipe_top_rect = self.pipe_top.get_rect(topleft=(0, 0))
        # отрисовываем колонны
        self.image = pygame.surface.Surface((self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap),
                                            pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        sprite_floor_height = assets.get_sprite('floor').get_rect().height
        min_y = 80
        max_y = configs.SCREEN_HEIGHT - sprite_floor_height - 80
        # создаем маску для колонны и флаг проета через колонну
        self.rect = self.image.get_rect(midleft=(configs.SCREEN_WIDTH, random.uniform(min_y, max_y)))
        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False
        super().__init__(*groups)

    # создаем следующие колонны
    def update_image(self, column_image):
        self.pipe_bottom = assets.get_sprite(column_image)
        self.pipe_top = pygame.transform.flip(self.pipe_bottom, False, True)

        self.image = pygame.surface.Surface(
            (self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap),
            pygame.SRCALPHA
        )
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 2
        if self.rect.right <= 0:
            self.kill()

    # функция следящая за пролетом через колонны
    def is_passed(self):
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False
