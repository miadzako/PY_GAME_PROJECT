import os  # библиотека для работы с ос
import pygame
import csv

sprites = {}  # словарь содержит все спрайты
audio = {}
results = []

pygame.mixer.init()


def load_sprites():
    path = os.path.join('assets', 'sprites')  # создает полный путь к директории с изображениями
    for item in os.listdir(path):  # перечисление файлов в этой директории
        sprites[item.split('.')[0]] = pygame.image.load(os.path.join(path, item))
        # подкрепляет изображения к соответствующему ключу в словаре


def get_sprite(name):
    return sprites[name]


def load_audios():
    path = os.path.join('assets', 'audio')
    for f in os.listdir(path):
        audio[f.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, f))


def play(name):
    audio[name].play()


