import pygame

from data.units import generation
from data.units.Pole import YAwareGroup, Board
from data.units.classes import Bullet, Box, Dno, Wall, Dno_Pers, Damager, Person
from data.units.generation import LEFT, RIGHT, UP, DOWN



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
    txt_level = (open(level).read()).split(';')

    boxes = dict()
    for i in range(len(txt_level)):
        if txt_level[i].split()[2] == 'box':
            box = txt_level[i].split()[:2]
            boxes.update({','.join(box): Box(box_spites, all_sprites, txt_level[i].split())})
            dno = Dno(dno_sprite, txt_level[i].split())
        else:
            wol = Wall(wol_sprites, all_sprites, txt_level[i].split())
            dno = Dno(dno_sprite, txt_level[i].split())
    damager = Damager(all_sprites, damager_group, board=board)
    person = Person(all_sprites, character_group, board=board)
    dno_person = Dno_Pers(dno_pers)
    person.rect.x, person.rect.y = coords


if __name__ == '__main__':
    pygame.init()
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    #  ------------------------------------------- изображения...
    logo = pygame.image.load('data/textures/Logo/logo3.png')
    #  -------------------------------------------
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
        pygame.display.flip()

    screen.fill((255, 255, 255))
    board = Board(screen, 1280, 720)

    li, lj = 2, 0
    map_list, map_str = generation.gen_map()
    print(*map_list, sep='\n')

    init_room(map_list[li][lj])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shooting = Bullet(bullet_group, character_group, person.rect, event.pos, screen, event,
                                  to=damager_group, txt_level=txt_level, dno_sprite=dno_sprite, board=board)
            if event.type == pygame.KEYDOWN:
                person.move(event.key)
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
            init_room(level, coord)
            board.render()

        board.three_on_four([person.rect.x, person.rect.y])
        board.three_on_four([damager.rect.x, damager.rect.y])
        # character_group.draw(screen)
        damager_group.update([person.rect.x,person.rect.y], txt_level, dno_sprite)
        character_group.update(txt_level, dno_sprite)
        bullet_group.update(txt_level, dno_sprite)
        all_sprites.draw(screen)
        bullet_group.draw(screen)
        pygame.draw.rect(screen, (25, 25, 25), [10, 10, 200, 20])
        pygame.draw.rect(screen, (255, 20, 25), [10, 10, (person.hp * 2), 20])
        hp_picture = pygame.image.load('data/textures/mini_object/Hp.png')
        screen.blit(hp_picture, (10, 10))
        pygame.display.flip()
    pygame.quit()
