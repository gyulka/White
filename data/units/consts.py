import pygame
a, b = 18, 32  # размеры комнат строки на столбцы
cell_size = 40  # размер 1 клетки(квадратная клетка)

RIGHT = '2'
LEFT = '4'
UP = '1'
DOWN = '3'


V=2


box1 = pygame.image.load('data/textures/object/box1.png')
box2 = pygame.image.load('data/textures/object/box2.png')
box3 = pygame.image.load('data/textures/object/box3.png')
box4 = pygame.image.load('data/textures/object/box4.png')
golv = pygame.image.load('data/textures/object/golv.png')
golv2 = pygame.image.load('data/textures/object/golv2.png')
golv3 = pygame.image.load('data/textures/object/golv3.png')
wol = pygame.image.load('data/textures/object/wol.png')
back = pygame.image.load('data/textures/mini_object/back.png')
pause = pygame.image.load('data/textures/mini_object/stop.png')
contin = pygame.image.load('data/textures/mini_object/continue.png')
image = {'box1': box1, 'box2': box2, 'box3': box3, 'box4': box4, 'golv': golv, 'golv2': golv2, 'golv3': golv3,
         'wol': wol}
