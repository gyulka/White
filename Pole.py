import pygame
box1 = pygame.image.load('files/textures/object/box1.png')
box2 = pygame.image.load('files/textures/object/box2.png')
box3 = pygame.image.load('files/textures/object/box3.png')
image = {'box1': box1, 'box2': box2, 'box3': box3}


class Board:
    def __init__(self, screen, width, size):
        self.screen = screen
        self.width = width // 40
        self.height = size // 40
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
                    self.screen.blit(image[self.pole[i * self.width + j][3]], (self.pole[i * self.width + j][1][0][0], self.pole[i * self.width + j][1][0][1] - 80))
                if self.pole[i * self.width + j][2] == 'sp':
                    pygame.draw.polygon(self.screen, (0, 255, 255), self.pole[i * self.width + j][1])

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
            y1 = (character[1] - 1) // 40 + 2
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
                self.screen.blit(image[txt[3]], (self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][0],
                                        self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][1] - 80))

    def all_coord(self):
        spisok = list()
        for i in range(len(self.pole)):
            spisok.append([[self.pole[i][0][0], self.pole[i][0][1]], [self.pole[i][0][0] + 40, self.pole[i][0][1] + 40]])
        return spisok

