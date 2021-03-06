import math
import random

import pygame

from data.units.consts import image, LEFT, UP, RIGHT, DOWN, V


class Bullet(pygame.sprite.Sprite):  # класс пули
    def __init__(self, group, bullets, otkuda, kuda, sc, event, txt_level, dno_sprite, to=False, otraj=3, board=None):
        super().__init__(group)
        self.to = to
        self.txt_level, self.dno_sprite = txt_level, dno_sprite
        self.board = board
        self.otkuda = otkuda
        self.kuda = kuda
        self.velocity = 10
        self.screen = sc
        self.fps = 60
        self.height, self.width = 1280, 720
        self.otraj = otraj
        self.kolvo_otraj = -1
        self.size_bullet = 8
        self.damage = random.randint(3, 8)
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
        self.update()

    def going(self):  # проверка на возможность движения
        collide_list = pygame.sprite.spritecollide(self, self.dno_sprite, False)
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
        if self.kolvo_otraj >= self.otraj:
            self.kill()
        self.pos = self.rect
        self.rect = self.rect.move(*self.moving)
        x = pygame.sprite.spritecollide(self, self.to, False)
        if x:
            for i in x:
                i.get_damage(self.damage)
            self.kill()

    def three_on_tree(self, cord):  # обновление поля вокруг пули (сектор 3*3)
        x, y = cord[0] // 40, cord[1] // 40
        self.all_sector = [[x - 1, y], [x, y], [x + 1, y],
                           [x, y + 1], [x + 1, y + 1], [x - 1, y + 1],
                           [x, y - 1], [x + 1, y - 1], [x - 1, y - 1]]
        for i in range(9):
            try:
                self.screen.blit(image[self.board.pole[self.all_sector[i][0]][self.all_sector[i][1]]],
                                 (self.all_sector[i][0] * 40, self.all_sector[i][1] * 40))
            except Exception:
                pass

    # def isshootedByPlayer(self):
    #     return self.shootedby
    #
    # def iscollidePlayer(self):
    #     if pygame.sprite.spritecollideany(self, self.to):
    #         return True
    #     return False


class Person(pygame.sprite.Sprite):  # класс игрока
    mandalorian_up1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_back_move1.png')
    mandalorian_up2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_back_move2.png')
    mandalorian_down1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_move1.png')
    mandalorian_down2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_move2.png')
    mandalorian_right1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_right_move1.png')
    mandalorian_right2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_right_move2.png')
    mandalorian_left1 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_left_move1.png')
    mandalorian_left2 = pygame.image.load('data/textures/main_charachter_1/Mandalorian_left_move2.png')
    damage = pygame.image.load('data/textures/mini_object/auh.png')

    def __init__(self, group, person, hp=100, board=None):
        super().__init__(group)
        self.old_hp = hp
        self.board = board
        self.add(person)
        self.dead = False
        self.dop = 10
        self.hp = hp
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

        self.dno_pers = pygame.sprite.Group()
        self.dno_person = Dno_Pers(self.dno_pers)

    def kill(self) -> None:
        super().kill()
        self.dno_person.kill()

    def move(self, event):  # кнопку нажали
        if event == 119:  # w
            self.kak[1] = - V
            self.check_pictures[1] = 1
            self.change_pictures[1] = -1
        if event == 97:  # a
            self.kak[0] = - V
            self.check_pictures[0] = 1
            self.change_pictures[0] = -1
        if event == 115:  # s
            self.kak[1] = V
            self.check_pictures[3] = 1
            self.change_pictures[3] = -1
        if event == 100:  # d
            self.kak[0] = V
            self.check_pictures[2] = 1
            self.change_pictures[2] = -1

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

    def going(self, txt_level, dno_sprite):  # проверка на возможность движения
        collide_list = pygame.sprite.spritecollide(self.dno_person, dno_sprite, False)
        if collide_list:
            return collide_list
        return False

    def change_image(self):
        if self.kak[0] > 0:
            self.change_pictures = [0] * 4
            self.check_pictures = [0] * 4
            self.check_pictures[2] = 1
        elif self.kak[0] < 0:
            self.change_pictures = [0] * 4
            self.check_pictures = [0] * 4
            self.check_pictures[0] = 1

        if self.kak[1] > 0:
            self.change_pictures = [0] * 4
            self.check_pictures = [0] * 4
            self.check_pictures[1] = 1
        elif self.kak[1] < 0:
            self.change_pictures = [0] * 4
            self.check_pictures = [0] * 4
            self.check_pictures[3] = 1

    def check_out(self):
        if self.rect.x <= -40:
            return LEFT
        if self.rect.x + self.rect.w >= 1280 + 40:
            return RIGHT
        if self.rect.y <= -50:
            return UP
        if self.rect.y + self.rect.h >= 770:
            return DOWN
        return None

    def update(self, *args):  # отрисовка перса
        image = None
        for i in enumerate(self.check_pictures):  # обновление картинки
            if i[1] != 0:
                if self.change_pictures[i[0]] >= 3:
                    image = self.puctures1[i[0]]
                    self.check_pictures[i[0]] = -1
                elif self.change_pictures[i[0]] < 0:
                    image = self.puctures2[i[0]]
                    self.check_pictures[i[0]] = 1
                self.change_pictures[i[0]] += i[1]
                break
        if image is not None:
            self.image = image
        if any(self.kak):
            self.rect.x += self.kak[0]
            self.dno_person.update(self.rect.x, self.rect.y)
            collide = self.going(*args)
            if collide:
                self.rect.x -= self.kak[0]
            self.rect.y += self.kak[1]
            self.dno_person.update(self.rect.x, self.rect.y)
            collide = self.going(*args)
            if collide:
                self.rect.y -= self.kak[1]
            self.dno_person.update(self.rect.x, self.rect.y)

    def get_damage(self, value):
        self.old_hp = self.hp
        self.hp -= value
        if self.hp <= 0:
            self.dead = True

    def can_anim_damage(self):
        if self.old_hp != self.hp:
            self.old_hp = self.hp
            return True
        else:
            return False

    def can_check_dead(self):
        return self.dead

    def check_the_end(self):
        return(self.rect.x + 20, self.rect.y + 80)


class Damager(Person):  # класс противников
    image = pygame.image.load('data/textures/not_friends/Shtoormovik.png')
    damager_up1 = pygame.image.load('data/textures/not_friends/Shtoormovik_move1.png')
    damager_up2 = pygame.image.load('data/textures/not_friends/Shtoormovik_move2.png')
    damager_down1 = pygame.image.load('data/textures/not_friends/Shtoormovik_move1.png')
    damager_down2 = pygame.image.load('data/textures/not_friends/Shtoormovik_move2.png')
    damager_right1 = pygame.image.load('data/textures/not_friends/Shtoormovik_right_move1.png')
    damager_right2 = pygame.image.load('data/textures/not_friends/Shtoormovik_right_move2.png')
    damager_left1 = pygame.image.load('data/textures/not_friends/Shtoormovik_left_move1.png')
    damager_left2 = pygame.image.load('data/textures/not_friends/Shtoormovik_left_move2.png')

    def __init__(self, all, vrag, person, txt_level, boxes, hp=30, pos=[620, 320], board=None, score=[0]):
        super().__init__(all, vrag, hp, board)
        self.score = score
        self.check_pictures = [0, 0, 0, 0]
        self.change_pictures = [0, 0, 0, 0]
        self.can_gun = 20
        self.person = person
        self.txt_level = txt_level
        self.puctures1 = [Damager.damager_left1, Damager.damager_up1,
                          Damager.damager_right1, Damager.damager_down1]
        self.puctures2 = [Damager.damager_left2, Damager.damager_up2,
                          Damager.damager_right2, Damager.damager_down2]
        self.rect.x = random.randint(40, 1200)
        self.rect.y = random.randint(40, 600)
        self.dno_person.rect.x = self.rect.x
        self.dno_person.rect.y = self.rect.y + 79
        while self.going(txt_level, boxes):
            self.rect.x = random.randint(40, 1200)
            self.rect.y = random.randint(40, 600)
            self.dno_person.rect.x = self.rect.x
            self.dno_person.rect.y = self.rect.y + 79
        self.skolko_go = random.randint(20, 30)
        self.skolko_going = 0
        self.kak = [random.choice([-2, 2, 0]), random.choice([-2, 2, 0])]
        if self.kak == [0, 0]:
            self.kak = [2, 0]
        self.image = Damager.image
        self.dead = False

    def get_damage(self, value):
        self.old_hp = self.hp
        self.hp -= value
        if self.hp <= 0:
            self.dead = True
            self.kill()

    def can_shoot(self):
        if self.dead:
            return False
        if self.can_gun == 0:
            self.can_gun = 20
            return True
        self.can_gun -= 1
        return False

    def kill(self) -> None:
        super().kill()
        self.dead = True
        self.score[0] += random.randint(5, 10)

    def check_person_in_vier_sector(self, person, txt_level):
        if (self.rect.x // 40 - 2 <= person.rect.x // 40 <= self.rect.x // 40 + 2
            and self.rect.y // 40 - 2 <= person.rect.y // 40 <= self.rect.y // 40 + 2) \
                or person.rect.x == self.rect.x or person.rect.y == self.rect.y:
            kuda = [person.rect.x, person.rect.y]
            otkuda = [self.rect.x, self.rect.y]
            try:
                alfa = math.atan(
                    (kuda[0] - otkuda[0]) / (
                            kuda[1] - otkuda[1]))  # нашли направление в градусной мере
                self.kak = [
                    -2 * math.sin(alfa) * (otkuda[1] - kuda[1]) // abs(
                        otkuda[1] - kuda[1]),
                    -2 * math.cos(alfa) * (otkuda[1] - kuda[1]) // abs(
                        otkuda[1] - kuda[1])]
            except Exception:
                self.kak = [-2, 0]
            return True
        return False

    def update(self, coord, *args):
        image = None
        for i in enumerate(self.check_pictures):  # обновление картинки
            if i[1] != 0:
                if self.change_pictures[i[0]] >= 3:
                    image = self.puctures1[i[0]]
                    self.check_pictures[i[0]] = -1
                elif self.change_pictures[i[0]] < 0:
                    image = self.puctures2[i[0]]
                    self.check_pictures[i[0]] = 1
                self.change_pictures[i[0]] += i[1]
                break
        if image is not None:
            self.image = image
        self.check_person_in_vier_sector(self.person, self.txt_level)
        if any(self.kak):
            self.rect.x += self.kak[0]
            self.skolko_going += 1
            self.dno_person.update(self.rect.x, self.rect.y)
            collide = self.going(*args)
            if collide:
                self.rect.x -= self.kak[0]
                self.skolko_go = self.skolko_going
            self.rect.y += self.kak[1]
            self.dno_person.update(self.rect.x, self.rect.y)
            collide = self.going(*args)
            if collide:
                self.rect.y -= self.kak[1]
                self.skolko_go = self.skolko_going
            self.dno_person.update(self.rect.x, self.rect.y)
            if self.skolko_go == self.skolko_going and not self.check_person_in_vier_sector(self.person,
                                                                                            self.txt_level):
                self.skolko_go = random.randint(20, 30)
                self.skolko_going = 0
                self.kak = [random.choice([-2, 2, 0]), random.choice([-2, 2, 0])]
                if self.kak == [0, 0]:
                    self.kak = [2, 0]
                self.change_image()


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
        if len(pos) < 2:
            self.kill()
        else:
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
        if len(pos) < 2:
            self.kill()
        else:
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
        if len(pos) < 2:
            self.kill()
        else:
            self.rect.x = int(pos[1]) * 40
            self.rect.y = int(pos[0]) * 40 + dop
            self.pos = self.rect
            self.dop = 10
