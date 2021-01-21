import pygame
import math
from Pole import Board

SIZE = (1280, 720)
SIZE_PERS = [55, 80]
SIZE_CELL = 40


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, bullets, otkuda, kuda, sc, event, otraj=3):
        super().__init__(group)
        self.add(bullets)
        self.otkuda = otkuda
        self.kuda = kuda
        self.velocity = 15
        self.screen = sc
        self.fps = 60
        self.height, self.width = SIZE
        self.otraj = otraj
        self.kolvo_otraj = -1
        self.size_bullet = 40
        #  возможно будет двигатся лишь на положительную сторону
        #  по оси у(тогда надо попробовать или иф или арксинус и теорему пифагора
        #  куда(?) нужно менять координату для каждого кадра
        self.alfa = math.atan(
            (self.kuda[0] - self.otkuda[0]) / (self.kuda[1] - self.otkuda[1]))  # нашли направление вектора(градус)
        self.moving = [
            -self.velocity * math.sin(self.alfa) * (self.otkuda[1] - self.kuda[1]) // abs(
                self.otkuda[1] - self.kuda[1]),
            -self.velocity * math.cos(self.alfa) * (self.otkuda[1] - self.kuda[1]) // abs(
                self.otkuda[1] - self.kuda[1])]
        self.image = pygame.image.load('files/textures/main_charachter_1/mandalorian.png')
        self.rect = self.image.get_rect()
        self.rect.x = otkuda[0]
        self.rect.y = otkuda[1]
        self.update(event)

    def update(self, *args):
        if self.rect.x >= self.height - self.size_bullet or self.rect.x <= 0:
            self.kolvo_otraj += 1
            self.moving[0] = - self.moving[0]
        if self.rect.y >= self.width - self.size_bullet or self.rect.y <= 0:
            self.kolvo_otraj += 1
            self.moving[1] = - self.moving[1]
        if self.kolvo_otraj == self.otraj or self.isshootedByPlayer():
            self.kill()
        self.rect = self.rect.move(*self.moving)

    def isshootedByPlayer(self):
        return False


class Person(pygame.sprite.Sprite):
    mandalorian1 = pygame.image.load('files/textures/main_charachter_1/mandalorian.png')
    mandalorian1_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_move1.png')
    mandalorian2_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_right_move1.png')
    mandalorian3_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_left_move1.png')
    mandalorian4_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_back_move1.png')

    def __init__(self, group, person):
        super.__init__(group)
        self.add(person)
        self.image = Person.mandalorian1
        self.rect = self.image.get_rect()
        self.rect.x = 620
        self.rect.y = 320

    def move(self, event):  # изменение какртинки в моем понимании произойдет на восьмом уроке, где нас этому научат
        if event == 119:  # w
            self.image = Person.mandalorian1_move1
            self.rect.x -= 2
        if event == 97:  # a
            self.image = Person.mandalorian3_move1
            self.rect.y -= 2
        if event == 115:  # s
            self.image = Person.mandalorian4_move1
            self.rect.x += 2
        if event == 100:  # d
            self.image = Person.mandalorian2_move1
            self.rect.y += 2
        if event == 101:
            print('инвентраь, я верю в него')


class Objects(pygame.sprite.Sprite):
    def __init__(self, group, object, pos, image):
        super.__init__(group)
        self.add(object)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]