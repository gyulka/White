import sys

import pygame
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication

import consts


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[0] = [1] * width
        self.board[-1] = [2] * width
        for i in range(height):
            if height - 1 > i > 0:
                self.board[i][0] = 2
                self.board[i][-1] = 2

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, screen, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.screen = screen

    def render(self):
        screen.fill((0, 0, 0))
        size = self.cell_size
        j = 0
        i = 0
        for i in range(self.height):
            for j in range(self.width):
                x = 0
                color = (0, 255, 0)
                if self.board[i][j] == 1:
                    color = (255, 0, 0)
                elif self.board[i][j] == 2:
                    color = (0, 0, 255)
                elif self.board[i][j] == 3:
                    color = (100, 100, 100)
                else:
                    x = 5

                pygame.draw.rect(self.screen, color,
                                 (self.top + size * j, self.left + size * i, size, size), x)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.func(cell)
        return cell

    def get_click1(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.func1(cell)
        return cell

    def get_cell(self, pos):
        pos = list(pos)
        if self.left < pos[0] < self.width * self.cell_size and self.top < pos[1] < self.height * self.cell_size:
            pos[0] -= self.left
            pos[1] -= self.top
            return (pos[1] // self.cell_size, pos[0] // self.cell_size)
        return None

    def func(self, pos):
        # if pos[0] != self.width - 1 and pos[0] != 0 and pos[1] != self.height and pos[1] != 0:
        self.board[pos[0]][pos[1]] = (self.board[pos[0]][pos[1]] + 1) % 3

    def func1(self, pos):
        self.board[pos[0]][pos[1]] = 3

    def save(self, text):
        print(self.board)
        dict1 = {1: 'wall', 2: 'box', 3: 'end'}
        f1 = open(text, 'w')
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]:
                    print(i, j, self.board[i][j])
                    f1.write(f'{i} {j} {dict1[self.board[i][j]]};')


class Mywidget(QWidget):
    pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    print(f'''s-save
n-new
red color-walls
blue color-boxes''')

    pygame.init()
    sys.excepthook = except_hook
    app = QApplication([])
    wid = Mywidget()

    size = (1280, 720)
    board = Board(consts.b, consts.a)
    screen = pygame.display.set_mode(size)
    board.set_view(screen, 5, 5, 40)
    board.render()
    pygame.display.flip()
    running = True
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                print(board.get_click(event.pos))
                board.render()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(board.get_click1(event.pos))
                board.render()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                board.save(QFileDialog.getSaveFileName(wid, 'Выбрать картинку', 'file.txt', '*.txt')[0])

            if event.type == pygame.QUIT:
                running = False
            pygame.display.flip()
    pygame.quit()
