import pygame
import math
from Pole import Board
from classes import Bullet, Person

SIZE = (1280, 720)
SIZE_PERS = [55, 80]
SIZE_CELL = 40

if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    person_sprites = pygame.sprite.Group()
    shoot_coord = list()
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    size_character = (40, 80)
    pos = (size[0] // 2 - size_character[0] // 2, size[1] // 2 - size_character[1] // 2)
    running = True
    logo = pygame.image.load('files/textures/Logo/logo.png')
    board = Board(screen, 1280, 720)
    board.render_pole()
    board.lvl('test_level.txt')
    screen.blit(logo, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(all_sprites, bullet_sprites, pos, event.pos, screen, event)
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.KEYUP:
                pass
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
