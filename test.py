import pygame
import math
from Pole import Board
from classes import Bullet, Person, BRD, Objects, Box

SIZE = (1280, 720)
SIZE_PERS = (40, 80)
SIZE_CELL = 40


class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.pos.y + spr.dop

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


def render_board():
    for w in range(SIZE[0] // SIZE_CELL):
        for h in range(SIZE[1] // SIZE_CELL):
            BRD(all_sprites, board_sprites, wall_horizon_sprites, wall_vertical_sprites, w, h)


def render_box():
    level = 'test_level.txt'
    txt_level = (open(level, mode='rt').read()).split(';')
    for i in range(len(txt_level)):
        txt = txt_level[i].split()
        Box(all_sprites, box_sprites, txt[0:2])
        Objects(all_sprites, object_sprites, draw_sprites, txt[0:2], txt[3])
        boxes.append([int(txt[0]) * 40, int(txt[1]) * 40 + 80])


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    draw_sprites = YAwareGroup()
    bullet_sprites = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    person_sprites = pygame.sprite.Group()
    object_sprites = pygame.sprite.Group()
    board_sprites = pygame.sprite.Group()
    wall_horizon_sprites = pygame.sprite.Group()
    wall_vertical_sprites = pygame.sprite.Group()
    shoot_coord = list()
    size = SIZE
    boxes = []
    dt = 0
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    size_character = SIZE_PERS
    pos = (size[0] // 2 - size_character[0] // 2, size[1] // 2 - size_character[1] // 2)
    running = True
    logo = pygame.image.load('files/textures/Logo/logo.png')
    board = Board(screen, *SIZE)
    board.render_pole()
    board.lvl('test_level.txt')
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
        all_sprites.draw(screen)
        pygame.display.flip()
    render_board()
    render_box()
    player = Person(all_sprites, person_sprites, wall_horizon_sprites, wall_vertical_sprites, draw_sprites,
                    box_sprites, boxes)
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(all_sprites, bullet_sprites, object_sprites, wall_horizon_sprites,
                                wall_vertical_sprites, player.rect, event.pos, screen, event)
            if event.type == pygame.KEYDOWN:
                player.move(event.key)
            if event.type == pygame.KEYUP:
                player.down(event.key)
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        draw_sprites.draw(screen)
        all_sprites.update(dt)
        pygame.display.flip()
    pygame.quit()
