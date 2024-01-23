import sys
import pygame
import assets
import column
import configs
import background
import floor
import bird
import game_over_meassage
import game_start_meassage
import score

# инициализируем шрифт для магазина
pygame.font.init()
# инициализируем главное окно
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
# флаги, позволяющие определять в каком состоянии игра
gameover = False
start = False
running_menu = True
# загрузка спрайтов
assets.load_sprites()
sprites = pygame.sprite.LayeredUpdates()
# флаг для определения, открыто ли меню
flag_menu = False
assets.load_audios()


# функция для создания спрайтов
def make_sprites():
    background.Background(0, sprites)
    background.Background(1, sprites)
    floor.Floor(0, sprites)
    floor.Floor(1, sprites)
    return bird.Bird(sprites), game_start_meassage.GameStart(sprites), score.Score(sprites)


# Инициализация спрайтов
new_bird, gsm, sc = make_sprites()
running = True
column_last_created_time = pygame.time.get_ticks()


# класс управляющий магазином
class Shop:
    def __init__(self, screen, background_instance_1, background_instance_2):
        self.screen = screen
        self.menu_background = pygame.image.load('assets/sprites/menu_background.jpg')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('MercutioNbpSmallcaps.ttf', 55)
        self.running_shop = False
        self.current_column_index = 0
        self.background_instances = [background_instance_1, background_instance_2]
        self.last_level_button_press_time = 0
        self.level_button_cooldown = 500
        # цвета, которые может принимать колонна
        self.column_images = [
            'assets/sprites/pipe-green.png',
            'assets/sprites/pipe-red.png'
        ]

        # кнопки в магазине
        self.buttons = [
            {'text': 'Цвет птицы', 'color': (222, 48, 0), 'action': self.switch_bird_color},
            {'text': 'Цвет колонн', 'color': (91, 156, 46), 'action': self.switch_column_color},
            {'text': 'Время суток', 'color': (72, 223, 237), 'action': self.switch_background_time}
        ]

        self.bird_color_index = 0
        self.column_color_index = 0
        self.background_color_index = 0

        # списки цветов для каждой кнопки
        self.bird_colors = [(222, 48, 0), (245, 178, 43), (75, 193, 248)]
        self.column_colors = [(91, 156, 46), (209, 103, 65)]
        self.background_colors = [(72, 223, 237), (0, 154, 168)]

    # функция отвечающая за смену цвета птицы
    def switch_bird_color(self):
        configs.current_bird_color_index = (configs.current_bird_color_index + 1) % len(
            configs.bird_colors)
        new_bird.update_color()

        self.bird_color_index = (self.bird_color_index + 1) % len(self.bird_colors)
        self.buttons[0]['color'] = pygame.Color(self.bird_colors[self.bird_color_index])

    # Обновление цвета птицы
    def update_bird_color(self):
        new_bird.update_color()

    # функция отвечающая за смену цвета колонн
    def switch_column_color(self):
        configs.current_column_color_index = (configs.current_column_color_index + 1) % len(configs.column_colors)
        self.current_column_index = (self.current_column_index + 1) % len(self.column_images)
        self.update_column_color()

        self.column_color_index = (self.column_color_index + 1) % len(self.column_colors)
        self.buttons[1]['color'] = pygame.Color(self.column_colors[self.column_color_index])

    # функция отвечающая за обновление колонн
    def update_column_color(self):
        configs.name_columns = configs.column_colors[configs.current_column_color_index]
        for sprite in sprites:
            if isinstance(sprite, column.Column):
                sprite.update_image(configs.name_columns)

    # функция отвечающая за смену времени для создания колонн
    def switch_background_time(self):
        configs.current_background_color_index = (configs.current_background_color_index + 1) % len(
            configs.background_colors)
        for background_instance in self.background_instances:
            background_instance.update_time()

        self.background_color_index = (self.background_color_index + 1) % len(self.background_colors)
        self.buttons[2]['color'] = pygame.Color(self.background_colors[self.background_color_index])

    # функция отвечающая за проверку возможности нажатия на кнопку
    def can_press_button(self):
        current_time_level = pygame.time.get_ticks()
        return current_time_level - self.last_level_button_press_time >= self.level_button_cooldown

    # функция отвечающая за запуск магазина
    def run_shop(self):
        while self.running_shop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                        self.running_shop = False

            self.screen.blit(self.menu_background, (0, 0))

            # Отображение кнопок в магазине
            button_height = 50
            button_spacing = 20
            total_height = len(self.buttons) * (button_height + button_spacing) - button_spacing
            start_y = (configs.SCREEN_HEIGHT - total_height) // 2
            # функция отвечающая за кнпоки в списке, их индексы
            for i, button in enumerate(self.buttons):
                button_rect = pygame.Rect((configs.SCREEN_WIDTH - 200) // 2 - 20,
                                          start_y + i * (button_height + button_spacing), 200 + 40, button_height)

                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (125, 125, 125), button_rect, border_radius=20)
                else:
                    pygame.draw.rect(self.screen, (112, 112, 112), button_rect, border_radius=20)
                # функция отвечающая за смену текста кнопок
                text_surface = self.font.render(button['text'], True, button['color'])
                text_rect = text_surface.get_rect(center=button_rect.center)
                self.screen.blit(text_surface, text_rect)

                if button_rect.collidepoint(pygame.mouse.get_pos()) and self.can_press_button():
                    if pygame.mouse.get_pressed()[0]:
                        button['action']()
                        self.last_level_button_press_time = pygame.time.get_ticks()

            pygame.display.flip()
            self.clock.tick(30)


# класс для управления меню
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.last_level_button_press_time = 0
        self.level_button_cooldown = 1000
        self.clock = pygame.time.Clock()
        self.menu_background = pygame.image.load('assets/sprites/menu_background.jpg')
        self.buttons = [
            {'default_image': 'assets/sprites/start_1.png', 'hover_image': 'assets/sprites/start_2.png',
             'action': self.start_game},
            {'default_image': 'assets/sprites/reset_1.png', 'hover_image': 'assets/sprites/reset_2.png',
             'action': self.reset_game},
            {'default_image': 'assets/sprites/level_mid.png', 'hover_image': 'assets/sprites/level_mid.png',
             'action': self.switch_level},
            {'default_image': 'assets/sprites/exit_1.png', 'hover_image': 'assets/sprites/exit_2.png',
             'action': self.exit_game}
        ]
        self.button_width = 200
        self.button_height = 90
        self.button_spacing = 30

    # повторяем функцию, чтобы можно было ссылаться на нее внутри класса
    def make_sprites(self):
        background.Background(0, sprites)
        background.Background(1, sprites)
        floor.Floor(0, sprites)
        floor.Floor(1, sprites)
        return bird.Bird(sprites), game_start_meassage.GameStart(sprites), score.Score(sprites)

    # функция отвечающая за смену уровня сложности
    def switch_level(self):
        # Изменение изображения кнопки level
        configs.current_level_index = (configs.current_level_index + 1) % len(configs.level_images)
        level_image_path = configs.level_images[configs.current_level_index]
        self.buttons[2]['default_image'] = level_image_path
        self.buttons[2]['hover_image'] = level_image_path

        configs.current_level_time_index = (configs.current_level_time_index + 1) % len(configs.level_time)

        # Обновление всех изменений
        self.update_button_images()

    # Метод для обновления изображений всех кнопок
    def update_button_images(self):
        for button in self.buttons:
            button['image'] = pygame.image.load(button['default_image'])

    # Продолжить игру
    def start_game(self):
        global start, running_menu
        start = True
        gsm.kill()
        pygame.time.set_timer(column_create_event, configs.level_time[configs.current_level_time_index])
        running_menu = False

    # Новая игра
    def reset_game(self):
        global start, gameover, sprites, new_bird, gsm, sc, column_last_created_time, \
            column_create_event, running_menu
        start = False
        gameover = False
        sprites.empty()
        new_bird.kill()
        new_bird, gsm, sc = make_sprites()
        column_last_created_time = pygame.time.get_ticks()
        pygame.time.set_timer(column_create_event, 0)
        running_menu = False

    def exit_game(self):
        pygame.quit()
        sys.exit()

    # проверем , может ли игрок нажать кнопку
    def can_press_button(self):
        current_time_level = pygame.time.get_ticks()
        return current_time_level - self.last_level_button_press_time >= self.level_button_cooldown

    # запускаем меню
    def run_menu(self):
        global running_menu, flag_menu
        flag_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            # рисуем задний фон меню
            self.screen.blit(self.menu_background, (0, 0))

            menu_height = (self.button_height + self.button_spacing) * len(self.buttons)
            menu_start_y = (self.screen.get_height() - menu_height) // 2
            # цикл позволяет обходить все кнопки в списке с доступом к индексам и значениям
            for i, button in enumerate(self.buttons):
                button_y = menu_start_y + i * (self.button_height + self.button_spacing)
                button_rect = pygame.Rect(25, button_y, self.button_width, self.button_height)
                # смена цвета кнопки
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    button['image'] = pygame.image.load(button['hover_image'])
                else:
                    button['image'] = pygame.image.load(button['default_image'])
                # вызываем действие кнопки
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0] and self.can_press_button():
                        button['action']()
                        self.last_level_button_press_time = pygame.time.get_ticks()
                self.screen.blit(button['image'], button_rect.topleft)

            pygame.display.flip()
            self.clock.tick(30)


background_instance_1 = background.Background(0, sprites)
background_instance_2 = background.Background(1, sprites)
menu = Menu(screen)
shop = Shop(screen, background_instance_1, background_instance_2)

# основной игровой цикл
while running:
    for event in pygame.event.get():
        # выход из игры
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # запуск игры
            if ((
                    event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.MOUSEBUTTONDOWN)
                    and not start and not gameover):
                start = True
                gsm.kill()
            # открытие меню
            if event.key == pygame.K_ESCAPE:
                running_menu = True
                menu.run_menu()
            # открытие магазина
            if event.key == pygame.K_b and not start and not gameover:
                shop.running_shop = True
                shop.run_shop()
            # управление птичкой
            if start and not gameover:
                new_bird.handle_event(event)
    # обновление всех спрайтов, их реакции на столкновения и прохождения
    if start and not gameover:
        sprites.update()
        if new_bird.check_collision(sprites):
            gameover = True
            start = False
            game_over_meassage.GameOver(sprites)
            pygame.time.set_timer(column_create_event, 0)
            assets.play('hit')
        # меняем результат игрока
        for sprite in sprites:
            if type(sprite) is column.Column and sprite.is_passed():
                sc.value += 1
                assets.play('point')

        if not flag_menu:
            current_time = pygame.time.get_ticks()
            time_since_last_column = current_time - column_last_created_time
            if configs.level_time[configs.current_level_time_index] <= time_since_last_column:
                column.Column(sprites)
                column_last_created_time = current_time
        else:
            column_last_created_time = pygame.time.get_ticks() - 500
            flag_menu = False

    sprites.draw(screen)
    # в случае проигрыша вызов кнопок для игры заново, выхода и окна окончания игры
    if gameover:
        game_over = game_over_meassage.GameOver(sprites)
        game_over.draw_buttons(screen)
        game_over.handle_event(event, sc.value)
        if game_over.handle_event(event, sc.value):
            start = False
            gameover = False
            sprites.empty()
            new_bird.kill()
            new_bird, gsm, sc = make_sprites()
            column_last_created_time = pygame.time.get_ticks()
            pygame.time.set_timer(column_create_event, 0)

    pygame.display.flip()
    clock.tick(configs.fps)

pygame.quit()
