import pygame
import consts

box1 = pygame.image.load('files/textures/object/box1.png')
box2 = pygame.image.load('files/textures/object/box2.png')
image = {'box1': box1, 'box2': box2}


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
                    self.pole.append([(i, j), coor, None, None])

    def lvl(self, level):  # создание значения уровня из вне по координатам.
        self.txt_level = (open(level, mode='rt').read()).split(';')
        for i in range(len(self.txt_level)):
            txt = self.txt_level[i].split()
            self.pole[int(txt[0]) * self.width + int(txt[1])][2] = txt[2]
            self.pole[int(txt[0]) * self.width + int(txt[1])][3] = txt[3]

    def render_level(self):  # тут уже рисуются объекты поля
        for i in range(self.height):
            for j in range(self.width):
                if self.pole[i * self.width + j][2] == 'box':
                    self.screen.blit(image[self.pole[i * self.width + j][3]], (
                        self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                if self.pole[i * self.width + j][2] == 'sp':
                    pygame.draw.polygon(self.screen, (0, 255, 255), self.pole[i * self.width + j][1])

    def check_in_stop(self, character):
        global sp
        sz = 38
        sum = 0
        znach = None
        for i in range(len(self.txt_level)):  # Проверка, в какой клетке находится игрок.
            txt = self.txt_level[i].split()
            cord = [self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][0],
                    self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][1]]
            if character[0] + 40 in range(cord[0], cord[0] + sz) and character[1] + 80 in range(cord[1],
                                                                                                cord[1] + sz + 3):
                sum += 1
            elif character[0] in range(cord[0], cord[0] + sz) and character[1] + 80 in range(cord[1], cord[1] + sz + 3):
                sum += 1
            elif character[0] in range(cord[0] - sz, cord[0] + sz) and character[1] + 80 in range(cord[1],
                                                                                                  cord[1] + sz + 3):
                sum += 1
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
        line = (pos[1] + 80) // 40
        for i in range(len(self.txt_level)):
            txt = self.txt_level[i].split()
            cord = self.pole[int(txt[0]) * self.width + int(txt[1])][0][0]
            if line == cord - 1 or line == cord - 2:
                self.screen.blit(image[txt[3]], (self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][0],
                                                 self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][1] - 80))


class Room(Board):
    def __init__(self, screen, width, size, a, b):
        super().__init__(screen, width, size)
        self.a = a
        self.b = b
        self.openFlag=True

    def close(self):
        self.openFlag = False
        #TODO при попытке перехода в слудующую комнату, действие совершаться не будет
        # восток, допилить


    def open(self):
        self.openFlag=True
        #TODO аналогично верхнему только в обратую сторону



