import pygame
import math
from Pole import Board

SIZE = (1280, 720)
SIZE_PERS = [55, 80]
SIZE_CELL = 40


class Bullet:
    def __init__(self, otkuda, kuda, sc):
        self.otkuda = otkuda
        self.kuda = kuda
        self.velocity = 10
        self.screen = sc
        self.fps = 60
        self.height, self.width = SIZE
        #  возможно будет двигатся лишь на положительную сторону
        #  по оси у(тогда надо попробовать или иф или арксинус и теорему пифагора
        #  куда(?) нужно менять координату для каждого кадра
        self.alfa = math.atan(
            (self.kuda[0] - self.otkuda[0]) / (self.kuda[1] - self.otkuda[1]))  # нашли направление вектора(градус)
        self.moving = [self.velocity * math.sin(self.alfa),
                       self.velocity * math.cos(self.alfa)]  # как изменяется координата
        # print(otkuda, kuda, SIZE, self.alfa, (self.kuda[0] - self.otkuda[0]), (self.kuda[1] - self.otkuda[1]), self.moving)
        self.render()

    def render(self):
        pygame.draw.rect(self.screen, (255, 255, 255), [self.otkuda[0] + self.moving[0], self.otkuda[1] + self.moving[1],
                                                      self.otkuda[0] + self.moving[0] + 10, self.otkuda[1] + self.moving[1] + 10], 0)

    def move_bullet(self):
        pass

    def isshootedByPlayer(self):
        pass


def move():
    global wait, pos, stap
    for i in flags:
        wait += 1
        if flags[i]:
            wait = 0
            image1 = mandalorian1_move1
            image2 = mandalorian1_move2
            check_and_break = False
            if i == pygame.K_w and board.check_in_stop((pos[0], pos[1] - sp)):
                if pos[1] - sp >= 1:
                    screen.fill((0, 0, 0))
                    board.render_level()
                    pos = (pos[0], pos[1] - sp)
                    image1 = mandalorian4_move1
                    image2 = mandalorian4_move2
                    check_and_break = True
            if i == pygame.K_a and board.check_in_stop((pos[0] - sp, pos[1])):
                if pos[0] - sp >= 1:
                    screen.fill((0, 0, 0))
                    board.render_level()
                    pos = (pos[0] - sp, pos[1])
                    image1 = mandalorian3_move1
                    image2 = mandalorian3_move2
                    check_and_break = True
            if i == pygame.K_s and board.check_in_stop((pos[0], pos[1] + sp)):
                if pos[1] < size[1] - size_character[1]:
                    screen.fill((0, 0, 0))
                    board.render_level()
                    pos = (pos[0], pos[1] + sp)
                    image1 = mandalorian1_move1
                    image2 = mandalorian1_move2
                    check_and_break = True
            if i == pygame.K_d and board.check_in_stop((pos[0] + sp, pos[1])):
                if pos[0] <= size[0] - size_character[0]:
                    screen.fill((0, 0, 0))
                    board.render_level()
                    pos = (pos[0] + sp, pos[1])
                    image1 = mandalorian2_move1
                    image2 = mandalorian2_move2
                    check_and_break = True
            if i and check_and_break:
                stap += 1
                if stap <= 20:
                    screen.blit(image1, pos)
                elif stap <= 40:
                    screen.blit(image2, pos)
                else:
                    screen.blit(image2, pos)
                    stap = 0
        if wait >= 50:
            screen.fill((0, 0, 0))
            board.render_level()
            screen.blit(mandalorian1, pos)
        board.on_line(pos)


def shoot(pos1, pos2):
    if pos1 != pos2:
        mimimum = min(pos1[0], pos2[0])
        coor1 = (pos1[0] - pos2[0]) / mimimum
        coor2 = (pos1[1] - pos2[1]) / mimimum
        sped = [coor1, coor2]
        shoot_coord.append([[pos1[0], pos1[1]], [pos2[0], pos2[1]], sped])


if __name__ == '__main__':
    pygame.init()
    shoot_coord = list()
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    size_character = (55, 80)
    pos = (size[0] // 2 - size_character[0] // 2, size[1] // 2 - size_character[1] // 2)
    pygame.display.flip()
    running = True
    flags = {}
    stap = 0
    s = ''
    wait = 0
    sp = 2
    smome = False
    logo = pygame.image.load('files/textures/Logo/logo.png')
    mandalorian1 = pygame.image.load('files/textures/main_charachter_1/mandalorian.png')
    mandalorian1_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_move1.png')
    mandalorian1_move2 = pygame.image.load('files/textures/main_charachter_1/mandalorian_move2.png')
    mandalorian1_shot = pygame.image.load('files/textures/main_charachter_1/mandalorian_shot.png')

    mandalorian2_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_right_move1.png')
    mandalorian2_move2 = pygame.image.load('files/textures/main_charachter_1/mandalorian_right_move2.png')
    mandalorian2_shot = pygame.image.load('files/textures/main_charachter_1/mandalorian_right_shot.png')

    mandalorian3_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_left_move1.png')
    mandalorian3_move2 = pygame.image.load('files/textures/main_charachter_1/mandalorian_left_move2.png')
    mandalorian3_shot = pygame.image.load('files/textures/main_charachter_1/mandalorian_left_shot.png')

    mandalorian4_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_back_move1.png')
    mandalorian4_move2 = pygame.image.load('files/textures/main_charachter_1/mandalorian_back_move2.png')
    board = Board(screen, 1280, 720)
    board.render_pole()
    board.lvl('test_level.txt')
    screen.blit(logo, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(pos, event.pos, screen)
            if event.type == pygame.KEYDOWN:
                flags[event.key] = True
                smome = True
            if event.type == pygame.KEYUP:
                flags[event.key] = False
        move()
        pygame.display.flip()
    pygame.quit()