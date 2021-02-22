import pygame
import os
import math
import consts
import random
box1 = pygame.image.load('data/textures/object/box1.png')
box2 = pygame.image.load('data/textures/object/box2.png')
box3 = pygame.image.load('data/textures/object/box3.png')
box4 = pygame.image.load('data/textures/object/box4.png')
golv = pygame.image.load('data/textures/object/golv.png')
golv2 = pygame.image.load('data/textures/object/golv2.png')
golv3 = pygame.image.load('data/textures/object/golv3.png')
wol = pygame.image.load('data/textures/object/wol.png')
image = {'box1': box1, 'box2': box2, 'box3': box3, 'box4': box4, 'golv': golv, 'golv2': golv2, 'golv3': golv3, 'wol': wol}


class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.pos.y + spr.dop

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


class Board:
    def __init__(self, screen, width, size):
        self.screen = screen
        self.width = consts.b
        self.height = consts.a
        self.cell_size = 0
        self.pole = [[random.choice(['golv', 'golv2', 'golv3']) for j in range(self.height)] for i in range(self.width)]
        self.txt_level = None
        for i in enumerate(self.pole):
            for j in enumerate(i[1]):
                self.screen.blit(image[j[1]], (i[0] * 40, j[0] * 40))

    def three_on_four(self, cord):
        x, y = cord[0] // 40, cord[1] // 40
        self.all_sector = [[x - 1, y], [x, y], [x + 1, y], [x + 2, y],
                      [x, y + 1], [x + 1, y + 1], [x + 2, y + 1], [x - 1, y + 1],
                      [x, y - 1], [x + 1, y - 1], [x + 2, y - 1], [x - 1, y - 1],
                      [x, y + 2], [x + 1, y + 2], [x + 2, y + 2], [x - 1, y + 2]]
        for i in range(16):
            try:
                self.screen.blit(image[self.pole[self.all_sector[i][0]][self.all_sector[i][1]]],
                             (self.all_sector[i][0] * 40, self.all_sector[i][1] * 40))
            except Exception:
                pass

    def get_boxes_in_sector(self, level):
        flag = [None] * 16
        for elem in enumerate(self.all_sector):
            if f'{elem[1][0]} {elem[1][1]} box' in level:
                flag[elem[0]] = elem[1]
        print(flag)
        return flag




class Box(pygame.sprite.Sprite):
    def __init__(self, obj, group, pos):
        super().__init__(group)
        self.add(obj)
        # self.image = pygame.Surface((40, 40))
        self.image = image[random.choice(['box1', 'box2', 'box3', 'box4'])]
        self.rect = self.image.get_rect()
        self.rect.w = 40
        self.rect.h = 40
        self.rect.width = 40
        self.rect.height = 40
        self.mask = pygame.mask.Mask(size=(40, 40), fill=True)
        self.mask.rect = [int(pos[1]) * 40, int(pos[0]) * 40 + 80]
        self.rect.x = int(pos[1]) * 40
        self.rect.y = int(pos[0]) * 40
        self.pos = self.rect
        self.dop = 10


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
            if i == pygame.K_w:
                if character.rect.y - sp >= 1:
                    character.rect.y -= sp
                    character.image = load_image('Mandalorian_back_move1.png')
                    check_and_break = True
            if i == pygame.K_a:
                if character.rect.x - sp >= 1:
                    character.rect.x -= sp
                    character.image = load_image('Mandalorian_left_move1.png')
                    check_and_break = True
            if i == pygame.K_s:
                if character.rect.y < size[1] - size_character[1]:
                    character.rect.y += sp
                    character.image = load_image('Mandalorian_move1.png')
                    check_and_break = True
            if i == pygame.K_d:
                if character.rect.x <= size[0] - size_character[0]:
                    character.rect.x += sp
                    character.image = load_image('Mandalorian_right_move1.png')
                    check_and_break = True

        x = board.get_boxes_in_sector(txt_level)
        for elem in x:
            if elem is not None:
                print(elem, boxes[','.join([str(i) for i in elem])])
                print(character.rect, boxes[','.join([str(i) for i in elem])].rect)
                if pygame.sprite.collide_mask(character, boxes[','.join([str(i) for i in elem])]):
                    character.rect.x = 0


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
    logo = pygame.image.load('data/textures/Logo/logo3.png')
    #  -------------------------------------------
    screen.blit(logo, (0, 0))
    splash = True  # заставка, ждем начала d.display.flip()
    all_sprites = YAwareGroup()
    character_group = pygame.sprite.Group()
    box_spites = pygame.sprite.Group()
    dno_sprite = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    img_character = load_image('Mandalorian.png')
    character = pygame.sprite.Sprite(character_group)
    character.image = img_character
    character.rect = character.image.get_rect()
    character.rect.x = 620
    character.rect.y = 320
    character.add(all_sprites)
    character.pos = character.rect
    character.dop = 10
    character.mask = pygame.mask.Mask(size=(40, 40), fill=True)

    # board.render_pole()
    # board.lvl('test_level.txt')
    screen.fill((255, 255, 255))
    board = Board(screen, 1280, 720)

    level = 'test_level.txt'
    txt_level = (open(level).read()).split(';')
    boxes = dict()
    for i in range(len(txt_level)):
        boxes.update({','.join(txt_level[i].split()[:2]): Box(box_spites, all_sprites, txt_level[i].split())})
    print(boxes)
    # board.render_level()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
                # shooting = Bullet(bullet_group, character_group, character.rect, event.pos, screen, event)
            if event.type == pygame.KEYDOWN:
                flags[event.key] = True
                smome = True
            if event.type == pygame.KEYUP:
                flags[event.key] = False
        move()
        board.three_on_four([character.rect.x, character.rect.y])
        character_group.draw(screen)
        all_sprites.draw(screen)
        # try:
        #     shooting.update()
        # except Exception:
        #     pass
        character_group.update(0)
        # bullet_group.draw(screen)
        # board.on_line([character.rect.x, character.rect.y])
        pygame.display.flip()
    pygame.quit()