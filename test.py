import pygame
from Pole import Board
import os


def load_image(name, color_key=None):  # Эта функция знакома всем до боли
    fullname = os.path.join(r'data\textures\main_charachter_1', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def move():
    global wait, pos, stap, character, character_group
    for i in flags:
        wait += 1
        if flags[i]:
            check_and_break = False
            if i == pygame.K_w and board.check_in_stop((character.rect.x, character.rect.y - sp)):
                if character.rect.y - sp >= 1:
                    character.rect.y -= sp
                    character.image = load_image('Mandalorian_back_move1.png')
                    check_and_break = True
            if i == pygame.K_a and board.check_in_stop((character.rect.x - sp, character.rect.y)):
                if character.rect.x - sp >= 1:
                    character.rect.x -= sp
                    character.image = load_image('Mandalorian_left_move1.png')
                    check_and_break = True
            if i == pygame.K_s and board.check_in_stop((character.rect.x, character.rect.y + sp)):
                if character.rect.y < size[1] - size_character[1]:
                    character.rect.y += sp
                    character.image = load_image('Mandalorian_move1.png')
                    check_and_break = True
            if i == pygame.K_d and board.check_in_stop((character.rect.x + sp, character.rect.y)):
                if character.rect.x <= size[0] - size_character[0]:
                    character.rect.x += sp
                    character.image = load_image('Mandalorian_right_move1.png')
                    check_and_break = True
            if i and check_and_break:
                pass


def shoot(pos1, pos2):
    if pos1 != pos2:
        mimimum = min(pos1[0], pos2[0])
        coor1 = (pos1[0] - pos2[0]) / mimimum
        coor2 = (pos1[1] - pos2[1]) / mimimum
        sped = [coor1, coor2]
        shoot_coord.append([[pos1[0], pos1[1]], [pos2[0], pos2[1]], sped])


if __name__ == '__main__':
    #  ------------------------------------------- Придвижу, что эта инфа никому не интересна
    pygame.init()
    shoot_coord = list()
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    size_character = (40, 80)
    pos = (size[0] // 2 - size_character[0] // 2, size[1] // 2 - size_character[1] // 2)
    running = True
    flags = {}
    stap = 0
    s = ''
    wait = 0
    sp = 2
    smome = False
    #  ------------------------------------------- изображения...
    logo = pygame.image.load('data/textures/Logo/logo.png')
    #  -------------------------------------------
    character_group = pygame.sprite.Group()
    img_character = load_image('Mandalorian.png')
    character = pygame.sprite.Sprite(character_group)
    character.image = img_character
    character.rect = character.image.get_rect()
    character.rect.x = 620
    character.rect.y = 320
    board = Board(screen, 1280, 720)
    board.render_pole()
    board.lvl('test_level.txt')
    screen.fill((255, 255, 255))
    board.render_level()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                flags[event.key] = True
                smome = True
            if event.type == pygame.KEYUP:
                flags[event.key] = False
        move()
        board.three_on_four([character.rect.x, character.rect.y])
        character_group.draw(screen)
        board.on_line([character.rect.x, character.rect.y])
        pygame.display.flip()
    pygame.quit()