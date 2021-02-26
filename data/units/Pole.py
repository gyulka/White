import random

import pygame

from data.units import consts


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
        self.render()

    def three_on_four(self, cord):  # отрисовка ближних обектов (4*4 вокруг персанажа
        x, y = cord[0] // 40, cord[1] // 40
        self.all_sector = [[x - 1, y], [x, y], [x + 1, y], [x + 2, y],
                           [x, y + 1], [x + 1, y + 1], [x + 2, y + 1], [x - 1, y + 1],
                           [x, y - 1], [x + 1, y - 1], [x + 2, y - 1], [x - 1, y - 1],
                           [x, y + 2], [x + 1, y + 2], [x + 2, y + 2], [x - 1, y + 2]]
        for i in range(16):
            try:
                self.screen.blit(consts.image[self.pole[self.all_sector[i][0]][self.all_sector[i][1]]],
                                 (self.all_sector[i][0] * 40, self.all_sector[i][1] * 40))
            except Exception:
                pass

    def get_boxes_in_sector(self, level, sector):  # выдает список коробок в секторе
        flag = [[None for i in range(int(len(sector) ** 0.5))] for _ in range(int(len(sector) ** 0.5))]
        for elem in enumerate(sector):
            if f'{elem[1][1]} {elem[1][0]} box' in level or f'{elem[1][1]} {elem[1][0]} wall' in level:
                print(elem[0], elem[1], elem[0] // int(len(sector) ** 0.5), elem[0] % int(len(sector) ** 0.5))
                flag[elem[0] // int(len(sector) ** 0.5)][elem[0] % int(len(sector) ** 0.5)] = elem[1]
        return flag

    def render(self):
        for i in enumerate(self.pole):
            for j in enumerate(i[1]):
                self.screen.blit(consts.image[j[1]], (i[0] * 40, j[0] * 40))


