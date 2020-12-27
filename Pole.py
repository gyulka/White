import pygame


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
                    self.pole.append([(i, j), coor, None])

    def lvl(self, level):  # создание значения уровня из вне по координатам.
        self.txt_level = (open(level, mode='rt').read()).split(';')
        for i in range(len(self.txt_level)):
            txt = self.txt_level[i].split()
            self.pole[int(txt[0]) * self.width + int(txt[1])][2] = txt[2]

    def render_level(self):  # тут уже рисуются объекты поля
        for i in range(self.height):
            for j in range(self.width):
                if self.pole[i * self.width + j][2] == 'box':
                    pygame.draw.polygon(self.screen, (0, 255, 0), self.pole[i * self.width + j][1])
                if self.pole[i * self.width + j][2] == 'sp':
                    pygame.draw.polygon(self.screen, (0, 255, 255), self.pole[i * self.width + j][1])

    def check_in_stop(self, character):
        sum = 0
        for i in range(len(self.txt_level)):
            if self.txt_level[i].split()[2] == 'box':
                txt = self.txt_level[i].split()
                cord = [self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][0],
                        self.pole[int(txt[0]) * self.width + int(txt[1])][1][0][1]]
                if character[0] + 55 in range(cord[0], cord[0] + 41) and character[1] + 80 in range(cord[1], cord[1] + 41):
                    sum += 1
                elif character[0] in range(cord[0], cord[0] + 41) and character[1] + 80 in range(cord[1], cord[1] + 41):
                    sum += 1
                elif character[0] + 55 in range(cord[0], cord[0] + 21) and character[1] + 80 in range(cord[1], cord[1] + 41):
                    sum += 1
                elif character[0] in range(cord[0] - 20, cord[0] + 41) and character[1] + 80 in range(cord[1], cord[1] + 41):
                    sum += 1
        if sum == 0:
            return True
        else:
            return False
