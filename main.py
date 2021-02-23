import math
import random

import pygame

import consts
import generation
from generation import LEFT, RIGHT, UP, DOWN

box1 = pygame.image.load('data/textures/object/box1.png')
box2 = pygame.image.load('data/textures/object/box2.png')
box3 = pygame.image.load('data/textures/object/box3.png')
box4 = pygame.image.load('data/textures/object/box4.png')
golv = pygame.image.load('data/textures/object/golv.png')
golv2 = pygame.image.load('data/textures/object/golv2.png')
golv3 = pygame.image.load('data/textures/object/golv3.png')
wol = pygame.image.load('data/textures/object/wol.png')
image = {'box1': box1, 'box2': box2, 'box3': box3, 'box4': box4, 'golv': golv, 'golv2': golv2, 'golv3': golv3,
         'wol': wol}


class YAwareGroup(pygame.sprite.Group):  # сортировка обектов для отрисовки сверху вниз
    def by_y(self, spr):
        return spr.pos.y + spr.dop

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


class Board:  # класс пола
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

    def three_on_four(self, cord):  # отрисовка ближних обектов (4*4 вокруг персанажа
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

    def get_boxes_in_sector(self, level, sector):  # выдает список коробок в секторе
        flag = [None] * len(sector)
        for elem in enumerate(sector):
            if f'{elem[1][1]} {elem[1][0]} box' in level or f'{elem[1][1]} {elem[1][0]} wall' in level:
                flag[elem[0]] = elem[1]
        return flag

    def render(self):
        for i in enumerate(self.pole):
            for j in enumerate(i[1]):
                self.screen.blit(image[j[1]], (i[0] * 40, j[0] * 40))


class Bullet(pygame.sprite.Sprite):  # класс пули
    def __init__(self, group, bullets, otkuda, kuda, sc, event, otraj=3):
        super().__init__(group)
        self.otkuda = otkuda
        self.kuda = kuda
        self.velocity = 10
        self.screen = sc
        self.fps = 60
        self.height, self.width = 1280, 720
        self.otraj = otraj
        self.kolvo_otraj = -1
        self.size_bullet = 8
        try:
            self.alfa = math.atan(
                (self.kuda[0] - self.otkuda[0]) / (self.kuda[1] - self.otkuda[1]))  # нашли направление в градусной мере
            self.moving = [
                -self.velocity * math.sin(self.alfa) * (self.otkuda[1] - self.kuda[1]) // abs(
                    self.otkuda[1] - self.kuda[1]),
                -self.velocity * math.cos(self.alfa) * (self.otkuda[1] - self.kuda[1]) // abs(
                    self.otkuda[1] - self.kuda[1])]
        except Exception:
            self.moving = [-10, 0]
        # направление пули в векторной мере(как изменятьпо х и у

        self.image = pygame.image.load('data/textures/mini_object/shoot1.png')
        self.rect = self.image.get_rect()
        self.rect.x = otkuda[0] + 16
        self.rect.y = otkuda[1] + 38
        self.update(event)

    def going(self):  # проверка на возможность движения
        x = board.get_boxes_in_sector(txt_level, self.all_sector)
        for elem in x:
            if elem is not None:
                elem = elem[::-1]
                collide_list = pygame.sprite.spritecollide(self, dno_sprite, False)
                if collide_list:
                    return collide_list
                return False

    def update(self, *args):  # изменение положения пули
        self.three_on_tree(self.rect)
        if any(self.moving):
            collide = self.going()
            if collide:
                self.kolvo_otraj += 1
                self.moving[0] = -self.moving[0]
            self.rect = self.rect.move(*self.moving)
            collide = self.going()
            if collide:
                self.kolvo_otraj += 1
                self.moving[1] = -self.moving[1]
                self.moving[0] = -self.moving[0]
        if self.kolvo_otraj >= self.otraj:
            self.kill()
        self.pos = self.rect
        self.rect = self.rect.move(*self.moving)

    def three_on_tree(self, cord):  # обновление поля вокруг пули (сектор 3*3)
        x, y = cord[0] // 40, cord[1] // 40
        self.all_sector = [[x - 1, y], [x, y], [x + 1, y],
                           [x, y + 1], [x + 1, y + 1], [x - 1, y + 1],
                           [x, y - 1], [x + 1, y - 1], [x - 1, y - 1]]
        for i in range(9):
            try:
                self.screen.blit(image[board.pole[self.all_sector[i][0]][self.all_sector[i][1]]],
                                 (self.all_sector[i][0] * 40, self.all_sector[i][1] * 40))
            except Exception:
                pass

    def isshootedByPlayer(self):
        return False


class Person(pygame.sprite.Sprite):  # класс игрока
    mandalorian_up1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_back_move1.png')
    mandalorian_up2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_back_move2.png')
    mandalorian_down1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_move1.png')
    mandalorian_down2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_move2.png')
    mandalorian_right1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_right_move1.png')
    mandalorian_right2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_right_move2.png')
    mandalorian_left1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_left_move1.png')
    mandalorian_left2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_left_move2.png')

    def __init__(self, group, person):
        super().__init__(group)
        self.add(person)
        self.dop = 10
        # изменение картинки
        self.check_pictures = [0, 0, 0, 0]
        self.change_pictures = [0, 0, 0, 0]
        self.puctures1 = [Person.mandalorian_left1, Person.mandalorian_up1,
                          Person.mandalorian_right1, Person.mandalorian_down1]
        self.puctures2 = [Person.mandalorian_left2, Person.mandalorian_up2,
                          Person.mandalorian_right2, Person.mandalorian_down2]
        self.image = pygame.image.load('data/textures/main_charachter_1/Mandalorian.png')
        self.rect = self.image.get_rect()
        self.rect.x = 620
        self.rect.y = 320
        self.kak = [0, 0]  # как менять координату перса
        self.pos = self.rect

    def move(self, event):  # кнопку нажали
        if event == 119:  # w
            self.kak[1] = - 2
            self.check_pictures[1] = 1
        if event == 97:  # a
            self.kak[0] = - 2
            self.check_pictures[0] = 1
        if event == 115:  # s
            self.kak[1] = 2
            self.check_pictures[3] = 1
        if event == 100:  # d
            self.kak[0] = 2
            self.check_pictures[2] = 1

    def down(self, event):  # кнопку отжали
        if event == 119:  # w
            self.kak[1] = 0
            self.check_pictures[1] = 0
        if event == 97:  # a
            self.kak[0] = 0
            self.check_pictures[0] = 0
        if event == 115:  # s
            self.kak[1] = 0
            self.check_pictures[3] = 0
        if event == 100:  # d
            self.kak[0] = 0
            self.check_pictures[2] = 0

    def going(self):  # проверка на возможность движения
        x = board.get_boxes_in_sector(txt_level, board.all_sector)
        for elem in x:
            if elem is not None:
                elem = elem[::-1]
                collide_list = pygame.sprite.spritecollide(dno_person, dno_sprite, False)
                if collide_list:
                    return collide_list
                return False

    def check_out(self):
        if self.rect.x <= -40:
            return LEFT
        if self.rect.x + self.rect.w >= 1280+40:
            return RIGHT
        if self.rect.y <= -50:
            return UP
        if self.rect.y + self.rect.h >= 770:
            return DOWN
        return None

    def update(self, *args):  # отрисовка перса
        for i in enumerate(self.check_pictures):  # обновление картинки
            if i[1]:
                if self.change_pictures[i[0]] == 40:
                    self.image = self.puctures1[i[0]]
        if any(self.kak):
            self.rect.x += self.kak[0]
            dno_person.update(self.rect.x, self.rect.y)
            collide = self.going()
            if collide:
                self.rect.x -= self.kak[0]
            self.rect.y += self.kak[1]
            dno_person.update(self.rect.x, self.rect.y)
            collide = self.going()
            if collide:
                self.rect.y -= self.kak[1]
            dno_person.update(self.rect.x, self.rect.y)


class Dno_Pers(pygame.sprite.Sprite):  # класс колайд-хитбокса
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface((38, 1))
        self.rect = self.image.get_rect()
        self.rect.x = 620
        self.rect.y = 320
        self.pos = self.rect

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y + 79


class Wall(pygame.sprite.Sprite):  # класс обектов
    def __init__(self, obj, group, pos):
        super().__init__(group)
        self.add(obj)
        self.image = image['wol']
        self.rect = self.image.get_rect()
        self.rect.w = 40
        self.rect.h = 40
        self.rect.width = 40
        self.rect.height = 40
        self.rect.x = int(pos[1]) * 40
        self.rect.y = int(pos[0]) * 40 - 79
        self.pos = self.rect
        self.dop = 10


class Box(pygame.sprite.Sprite):  # класс обектов
    def __init__(self, obj, group, pos):
        super().__init__(group)
        self.add(obj)
        self.image = image[random.choice(['box1', 'box2', 'box3', 'box4'])]
        self.rect = self.image.get_rect()
        self.rect.w = 40
        self.rect.h = 40
        self.rect.width = 40
        self.rect.height = 40
        self.rect.x = int(pos[1]) * 40
        self.rect.y = int(pos[0]) * 40 - 79
        self.pos = self.rect
        self.dop = 10


class Dno(pygame.sprite.Sprite):  # класс хитбоксов обектов
    def __init__(self, group, pos, dop=0):
        super().__init__(group)
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.rect.w = 40
        self.rect.h = 40
        self.rect.width = 40
        self.rect.height = 40
        self.rect.x = int(pos[1]) * 40
        self.rect.y = int(pos[0]) * 40 + dop
        self.pos = self.rect
        self.dop = 10


#


#
# def load_image(name, color_key=None):  # Эта функция знакома всем до боли
#     fullname = os.path.join(r'data\textures\main_charachter_1', name)
#     try:
#         image = pygame.image.load(fullname)
#     except pygame.error as message:
#         print('Cannot load image:', name)
#         raise SystemExit(message)
#
#     if color_key is not None:
#         if color_key == -1:
#             color_key = image.get_at((0, 0))
#         image.set_colorkey(color_key)
#     else:
#         image = image.convert_alpha()
#     return image


def init_room(stroka='files/levels/0_2_1.txt', coords=[1280 // 2, 720 // 2]):
    global all_sprites, character_group, dno_pers, dno_sprite, box_spites, bullet_group, level, txt_level, boxes, person, dno_person
    all_sprites = YAwareGroup()

    character_group = pygame.sprite.Group()
    dno_pers = pygame.sprite.Group()
    dno_sprite = pygame.sprite.Group()
    box_spites = pygame.sprite.Group()
    wol_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    level = stroka
    txt_level = (open(level).read()).split(';')

    boxes = dict()
    for i in range(len(txt_level)):
        if txt_level[i].split()[2] == 'box':
            box = txt_level[i].split()[:2]
            boxes.update({','.join(box): Box(box_spites, all_sprites, txt_level[i].split())})
            dno = Dno(dno_sprite, txt_level[i].split())
        else:
            wol = Wall(wol_sprites, all_sprites, txt_level[i].split())
            dno = Dno(dno_sprite, txt_level[i].split())
    person = Person(all_sprites, character_group)
    dno_person = Dno_Pers(dno_pers)
    person.rect.x, person.rect.y = coords


if __name__ == '__main__':
    pygame.init()
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    #  ------------------------------------------- изображения...
    logo = pygame.image.load('data/textures/Logo/logo3.png')
    #  -------------------------------------------
    screen.blit(logo, (0, 0))
    splash = True  # заставка, ждем начала игры
    while splash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                splash = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                splash = False
            if event.type == pygame.KEYDOWN:
                splash = False
        pygame.display.flip()

    screen.fill((255, 255, 255))
    board = Board(screen, 1280, 720)

    li, lj = 2, 0
    map_list, map_str = generation.gen_map()
    print(*map_list, sep='\n')

    init_room(map_list[li][lj])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shooting = Bullet(bullet_group, character_group, person.rect, event.pos, screen, event)
            if event.type == pygame.KEYDOWN:
                person.move(event.key)
            if event.type == pygame.KEYUP:
                person.down(event.key)
        ans = person.check_out()
        if ans is not None:
            if ans == UP:
                li -= 1
                coord = [person.rect.x, 640]
            elif ans == RIGHT:
                lj += 1
                coord = [0, person.rect.y]
            elif ans == DOWN:
                li += 1
                coord = [person.rect.x, 40]
            elif ans == LEFT:
                lj -= 1
                coord = [1240, person.rect.y]

            level = map_list[li][lj]
            init_room(level, coord)
            board.render()

        board.three_on_four([person.rect.x, person.rect.y])
        character_group.draw(screen)
        character_group.update(0)
        bullet_group.update(0)
        all_sprites.draw(screen)
        bullet_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
