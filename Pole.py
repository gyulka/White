import pygame

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


class Board:
    def __init__(self, screen, width, size):
        self.screen = screen
        self.width = consts.b
        self.height = consts.a
        self.cell_size = 40
        self.pole = list()
        self.txt_level = None

    def render_pole(self):  # ВНИМАНИЕ!!! ПРОСТО ЗАДАЮТСЯ ЗНАЧЕНИЯ КАЖДОЙ КЛЕТКИ, НЕ РИСУЕТ НИ ЧЕГО!!
        for i in range(self.height):
            for j in range(self.width):
                coor1 = j * self.cell_size
                coor2 = i * self.cell_size
                coor3 = (j + 1) * self.cell_size
                coor4 = (i + 1) * self.cell_size
                coor = ((coor1, coor2), (coor3, coor2), (coor3, coor4), (coor1, coor4))
                if len(self.pole) != self.width * self.height:
                    self.pole.append([(i, j), coor, None, 'golv'])

    def lvl(self, level):  # создание значения уровня из вне по координатам.
        self.txt_level = (open(level, mode='rt').read()).split(';')
        for i in range(len(self.txt_level)):
            txt = self.txt_level[i].split()
            self.pole[int(txt[0]) * self.width + int(txt[1])][2] = txt[2]
            randomwol = random.choice(['box1', 'box2', 'box3', 'box4'])
            self.pole[int(txt[0]) * self.width + int(txt[1])][3] = randomwol

    def render_level(self):  # тут уже рисуются объекты поля, один раз используется
        for i in range(self.height):
            for j in range(self.width):
                if self.pole[i * self.width + j][2] == 'box':
                    self.screen.blit(golv, (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                    self.screen.blit(image[self.pole[i * self.width + j][3]], (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                if self.pole[i * self.width + j][2] == 'wall':
                    self.screen.blit(golv, (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                    self.screen.blit(image['wol'], (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                    self.pole[i * self.width + j][3] = 'wol'
                elif self.pole[i * self.width + j][2] != 'box':
                    randomwol = random.choice(['golv', 'golv2', 'golv3'])
                    self.screen.blit(image[randomwol], (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                    self.pole[i * self.width + j][3] = randomwol

    def three_on_four(self, cord):
        sector1 = (cord[1] // 40, cord[0] // 40)
        sector2 = ((cord[1] + 80) // 40 - 1, cord[0] // 40)
        sector3 = ((cord[1] + 80) // 40, cord[0] // 40)
        sector4 = (cord[1] // 40, (cord[0] + 40) // 40)
        sector5 = ((cord[1] + 80) // 40 - 1, (cord[0] + 40) // 40)
        sector6 = ((cord[1] + 80) // 40, (cord[0] + 40) // 40)
        sector7 = (cord[1] // 40, cord[0] // 40 - 1)
        sector8 = ((cord[1] + 80) // 40 - 1, cord[0] // 40 - 1)
        sector9 = ((cord[1] + 80) // 40, cord[0] // 40 - 1)
        sector10 = (cord[1] // 40 - 1, (cord[0] + 40) // 40)
        sector11 = ((cord[1] + 80) // 40 - 3, (cord[0] + 40) // 40 - 1)
        sector12 = ((cord[1] + 80) // 40 - 3, (cord[0] + 40) // 40 - 2)
        all_sector = [sector1,  sector2, sector3, sector4, sector5, sector6, sector7, sector8, sector9, sector10, sector11, sector12]
        for i in range(self.height):
            for j in range(self.width):
                if self.pole[i * self.width + j][0] in all_sector and self.pole[i * self.width + j][3] != None and self.pole[i * self.width + j][3] != 'box':
                    self.screen.blit(image[self.pole[i * self.width + j][3]], (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                if self.pole[i * self.width + j][2] == 'box':
                    self.screen.blit(golv, (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                    self.screen.blit(image[self.pole[i * self.width + j][3]], (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))

    def check_in_stop(self, character):
        global sp
        sum = 0
        znach = None
        for i in range(len(self.txt_level)):  # Проверка, в какой клетке находится игрок.
            txt = self.txt_level[i].split()
            cord = [self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][0],
                    self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][1]]
            x1, y1 = character[0] + 2, character[1] + 80
            if (((x1 + 38 > cord[0] and x1 + 42 < cord[0] + 40) or (x1 > cord[0] and x1 < cord[0] - 40)) and (y1 >= cord[1] and y1 <= cord[1] + 40)):
                sum += 1
            x1, y1 = character[0] - 42, character[1] + 80
            if (((x1 + 38 > cord[0] and x1 + 42 < cord[0] + 40) or (x1 > cord[0] and x1 < cord[0] - 40)) and (y1 >= cord[1] and y1 <= cord[1] + 40)):
                sum += 1
            x1 = (character[0] + 20) // 40
            y1 = (character[1] - 4) // 40 + 2
            y2 = (character[1]) // 40 + 2
            for i in range(len(self.txt_level)):
                txt = self.txt_level[i].split()
                if (txt[0] == str(y1) or txt[0] == str(y2)) and txt[1] == str(x1) and txt[2] == 'box':
                    sum += 1
                    break
            if sum != 0:
                znach = self.txt_level[i].split()[2]
                break
        if znach == 'box':
            return False
        elif znach == 'sp':
            sp = 10
            return True
        else:
            sp = 2
            return True

    def on_line(self, pos):  # РЕАЛИЗМ!!!!!!!!
        x1 = (pos[0] + 20) // 40
        y1 = (pos[1]) // 40 + 2
        for i in range(len(self.txt_level)):
            txt = self.txt_level[i].split()
            cord = self.pole[int(txt[0]) * self.width + int(txt[1])][0][0]
            cord2 = self.pole[int(txt[0]) * self.width + int(txt[1])][0][1]
            if (x1 == cord2 or x1 == cord2 - 1 or x1 == cord2 + 1) and y1 <= cord:
                for j in range(len(self.pole)):
                    if (cord, cord2) == self.pole[j][0]:
                        img = self.pole[j][3]
                        break
                self.screen.blit(image[img], (self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][0],
                                        self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][1] - 80))

    def all_coord(self):
        spisok = list()
        for i in range(len(self.pole)):
            spisok.append([[self.pole[i][0][0], self.pole[i][0][1]], [self.pole[i][0][0] + 40, self.pole[i][0][1] + 40]])
        return spisok

