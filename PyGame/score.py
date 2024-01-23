import pygame.sprite
import layer, assets, configs


# функция отвечающая за показ счета
class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = layer.Layer.INTERFACE
        self.value = 0
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)
        self.__create()
        super().__init__(*groups)

    # отображение счета через спрайты
    # смотрим зачения sc
    def __create(self):
        self.str_value = str(self.value)
        self.images = []
        self.width = 0
        for str_value_char in self.str_value:
            img = assets.get_sprite(str_value_char)
            self.images.append(img)
            self.width += img.get_width()
        self.height = self.images[0].get_height()
        self.image = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, 50))
        offset = 0
        for img in self.images:
            self.image.blit(img, (offset, 0))
            offset += img.get_width()

    # после каждого пролета колонны обновляем счет
    def update(self):
        self.__create()
