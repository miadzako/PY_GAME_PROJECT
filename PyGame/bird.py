import pygame.sprite

import assets
import column
import configs
import floor
import layer


class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = layer.Layer.PLAYER  # задание слоя спрайта

        # загрузка изображений птицы с учетом текущего цвета
        self.images = [assets.get_sprite(f'{configs.bird_colors[configs.current_bird_color_index]}-upflap'),
                       assets.get_sprite(f'{configs.bird_colors[configs.current_bird_color_index]}-midflap'),
                       assets.get_sprite(f'{configs.bird_colors[configs.current_bird_color_index]}-downflap')]

        self.image = self.images[0]  # установка текущего изображения
        self.rect = self.image.get_rect(topleft=(-50, 50))
        self.flap = 0
        self.mask = pygame.mask.from_surface(self.image)  # создание маски для определения столкновений
        super().__init__(*groups)

    def update(self):  # метод обновления состояния птицы
        self.images.insert(0, self.images.pop())  # анимация маха крыльев
        self.image = self.images[0]

        self.flap += configs.GRAVITY
        self.rect.y += self.flap  # перемещение птицы по вертикали

        if self.rect.x < 50:
            self.rect.x += 3

    def handle_event(self, event):
        if (event.type == pygame.KEYDOWN and
                (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP)):
            self.flap = 0
            self.flap -= 6  # полёт птицы после нажатия определенных кнопок
            assets.play('wing')

    def check_collision(self, sprites):  # метод проверки столкновений с другими спрайтами
        for sprite in sprites:
            if ((type(sprite) is column.Column or type(sprite) is floor.Floor) and
                    sprite.mask.overlap(self.mask, (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)) or
                    self.rect.bottom < 0):
                return True
        return False

    def update_color(self):  # метод обновления цвета птицы
        bird_color = configs.bird_colors[configs.current_bird_color_index]
        # обновление изображений птицы с учетом нового цвета
        self.images = [assets.get_sprite(f'{bird_color}-upflap'),
                       assets.get_sprite(f'{bird_color}-midflap'),
                       assets.get_sprite(f'{bird_color}-downflap')]
        self.image = self.images[0]