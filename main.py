import pygame
import random

from data.units import generation
from data.units.Pole import YAwareGroup, Board
from data.units.classes import Bullet, Box, Dno, Wall, Dno_Pers, Damager, Person
from data.units.generation import LEFT, RIGHT, UP, DOWN
from data.units.consts import back, pause, contin


def init_room(stroka='files/levels/0_2_1.txt', coords=[1280 // 2, 720 // 2]):
    global all_sprites, character_group, dno_pers, dno_sprite, box_spites, bullet_group, level, txt_level, boxes, person, dno_person, damager_group, damager
    all_sprites = YAwareGroup()
    character_group = pygame.sprite.Group()
    damager_group = pygame.sprite.Group()
    dno_pers = pygame.sprite.Group()
    dno_sprite = pygame.sprite.Group()
    box_spites = pygame.sprite.Group()
    wol_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    level = stroka
    txt_level = (open(level).read()).rstrip('\n').split(';')


    # boxes = dict()
    for i in range(len(txt_level)):

        if txt_level[i] and txt_level[i].split()[2] == 'box':
            box =Box(box_spites, all_sprites, txt_level[i].split())

            dno = Dno(dno_sprite, txt_level[i].split())
        else:
            wol = Wall(wol_sprites, all_sprites, txt_level[i].split())
            dno = Dno(dno_sprite, txt_level[i].split())
    damager = Damager(all_sprites, damager_group, board=board)
    person = Person(all_sprites, character_group, board=board)
    dno_person = Dno_Pers(dno_pers)
    person.rect.x, person.rect.y = coords


def Menu():
    global sl_start, stop, board, li, lj, map_list, map_str, running
    screen.blit(logo, (0, 0))
    timer = pygame.time.Clock()
    pygame.display.flip()
    timer.tick(1)
    screen.blit(manda_logo, (0, 0))
    pygame.display.flip()
    timer.tick(1)
    screen.blit(menu, (0, 0))
    pygame.display.flip()
    wh_game = True
    sl_start = False
    ex = False
    while wh_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wh_game = False
                running = False
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] in range(1048, 1248) and event.pos[1] in range(605, 645):
                    screen.blit(select, (1048, 605))
                    sl_start = True
                elif event.pos[0] in range(1048, 1248) and event.pos[1] in range(658, 698):
                    screen.blit(select, (1048, 658))
                    sl_start = True
                elif event.pos[0] in range(8, 155) and event.pos[1] in range(667, 712):
                    screen.blit(select3, (8, 667))
                    ex = True
                else:
                    screen.blit(menu, (0, 0))
                    sl_start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sl_start:
                    wh_game = False
                    stop = False
                elif ex:
                    wh_game = False
                    running = False
        pygame.display.flip()
    screen.fill((255, 255, 255))
    board = Board(screen, 1280, 720)

    li, lj = 2, 0
    map_list, map_str = generation.gen_map()
    print(*map_list, sep='\n')

    init_room(map_list[li][lj])


if __name__ == '__main__':
    pygame.init()
    stop = True
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    #  ------------------------------------------- изображения...
    logo = pygame.image.load(random.choice(['data/textures/Logo/logo3.png', 'data/textures/Logo/logo.png', 'data/textures/Logo/logo2.png']))
    manda_logo = pygame.image.load('data/textures/Logo/Mand.png')
    menu = pygame.image.load('data/textures/Logo/menu.png')
    select = pygame.image.load('data/textures/mini_object/select.png')
    select2 = pygame.image.load('data/textures/mini_object/select2.png')
    select3 = pygame.image.load('data/textures/mini_object/select3.png')
    #  -------------------------------------------
    Menu()

    def Pause():
        global stop
        if stop:
            stop = False
            board.render_all_map()
        else:
            stop = True
            board.render_all_map()
            screen.blit(back, (0, 0))
            screen.blit(contin, (1220, 30))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION and stop:
                if stop and event.pos[0] in range(540, 740) and event.pos[1] in range(379, 419):
                    screen.blit(select, (540, 379))
                elif stop and event.pos[0] in range(501, 779) and event.pos[1] in range(327, 367):
                    screen.blit(select2, (501, 327))
                else:
                    board.render_all_map()
                    screen.blit(back, (0, 0))
                    screen.blit(contin, (1220, 30))
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if stop and event.pos[0] in range(501, 779) and event.pos[1] in range(327, 367):
                    Menu()
                x = event.pos[0]
                y = event.pos[1]
                if event.button == 1:
                    if x in range(1220, 1251) and y in range(30, 51):
                        Pause()
                    elif x not in range(1220, 1251) and y not in range(30, 51) and not stop:
                        shooting = Bullet(bullet_group, character_group, person.rect, event.pos, screen, event,
                                          to=damager_group, txt_level=txt_level, dno_sprite=dno_sprite, board=board)
            if event.type == pygame.KEYDOWN:
                person.move(event.key)
                if event.key == 27:
                    Pause()
            if event.type == pygame.KEYUP:
                person.down(event.key)
        ans = person.check_out()
        if ans is not None:
            if ans == UP:
                li -= 1
                coord = [person.rect.x, 640]
            elif ans == RIGHT:
                lj += 1
                coord = [0, person.rect.y]
            elif ans == DOWN:
                li += 1
                coord = [person.rect.x, 0]
            elif ans == LEFT:
                lj -= 1
                coord = [1240, person.rect.y]

            level = map_list[li][lj]
            print(level)
            init_room(level, coord)
            board.render()

        if not stop:
            board.three_on_four([person.rect.x, person.rect.y])
            character_group.draw(screen)
            damager_group.update([person.rect.x,person.rect.y], txt_level, dno_sprite)
            character_group.update(txt_level, dno_sprite)
            bullet_group.update(txt_level, dno_sprite)
            all_sprites.draw(screen)
            bullet_group.draw(screen)
            pygame.draw.rect(screen, (25, 25, 25), [10, 10, 200, 20])
            pygame.draw.rect(screen, (255, 20, 25), [10, 10, (person.hp * 2), 20])
            hp_picture = pygame.image.load('data/textures/mini_object/Hp.png')
            screen.blit(hp_picture, (10, 10))
            screen.blit(pause, (1220, 30))

        pygame.display.flip()
    pygame.quit()
