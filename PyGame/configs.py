#здесь прописаны названия скинов и констант
name_bird = 'redbird'
name_background = 'background-day'
name_columns = 'pipe-green'
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 510
fps = 60
GRAVITY = 0.4
level_time = [2000, 1500, 1000]
level_images = ['assets/sprites/level_ez.png', 'assets/sprites/level_mid.png', 'assets/sprites/level_hard.png']
current_level_index = 1  # Индекс текущего уровня (по умолчанию mid)
current_level_time_index = 1

bird_colors = ['redbird', 'yellowbird', 'bluebird']
current_bird_color_index = 0

background_colors = ['background-day', 'background-night']
current_background_color_index = 0

column_colors = ['pipe-green', 'pipe-red']
current_column_color_index = 0
name_columns = column_colors[current_column_color_index]