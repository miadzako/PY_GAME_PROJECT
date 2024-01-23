import pygame.sprite

import assets
import configs
import layer  # модуль для определения слоев спрайтов


class Background(pygame.sprite.Sprite):
    def __init__(self, k, *groups):
        # инициализация класса
        self._layer = layer.Layer.BACKGROUND  # установка слоя спрайта
        # загрузка изображения фона в зависимости от текущего времени суток
        self.image = assets.get_sprite(f'{configs.background_colors[configs.current_background_color_index]}')
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH * k, 0))
        super().__init__(*groups)  # вызов родительского класса для добавления спрайта в группы

    def update(self):
        # обновление положения спрайта
        self.rect.x -= 1
        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH

    # смотрим за временем для дальнейшего создания колонн
    def update_time(self):
        background_time = configs.background_colors[configs.current_background_color_index]
        self.image = assets.get_sprite(f'{background_time}')
