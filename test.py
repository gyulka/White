import pygame


def move():
    global wait, pos, stap
    for i in flags:
        wait += 1
        if flags[i]:
            wait = 0
            image1 = mandalorian1_move1
            image2 = mandalorian1_move2
            check_and_break = False
            if i == pygame.K_w:
                if pos[1] - 1 >= 1:
                    screen.fill((0, 0, 0))
                    pos = (pos[0], pos[1] - 1)
                    image1 = mandalorian4_move1
                    image2 = mandalorian4_move2
                    check_and_break = True
            if i == pygame.K_a:
                if pos[0] - 1 >= 1:
                    screen.fill((0, 0, 0))
                    pos = (pos[0] - 1, pos[1])
                    image1 = mandalorian3_move1
                    image2 = mandalorian3_move2
                    check_and_break = True
            if i == pygame.K_s:
                if pos[1] < size[1] - size_character[1]:
                    screen.fill((0, 0, 0))
                    pos = (pos[0], pos[1] + 1)
                    image1 = mandalorian1_move1
                    image2 = mandalorian1_move2
                    check_and_break = True
            if i == pygame.K_d:
                if pos[0] <= size[0] - size_character[0]:
                    screen.fill((0, 0, 0))
                    pos = (pos[0] + 1, pos[1])
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
            screen.blit(mandalorian1, pos)


def shoot(pos1, pos2):
    shoot_coord.append([[pos1[0], pos1[1]], [pos2[0], pos2[1]], 0])


if __name__ == '__main__':
    pygame.init()
    shoot_coord = list()
    size = (1000, 1000)
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
    screen.blit(mandalorian1, pos)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot(event.pos, pos)
            if event.type == pygame.KEYDOWN:
                flags[event.key] = True
            if event.type == pygame.KEYUP:
                flags[event.key] = False
        move()
        rem = list()
        for i in range(len(shoot_coord)):
            if shoot_coord[i][2] <= 50:
                pygame.draw.line(screen, (255, 0, 0), shoot_coord[i][0], shoot_coord[i][1])
                shoot_coord[i][2] = shoot_coord[i][2] + 1
            else:
                rem.append(shoot_coord[i])
        for i in range(len(rem)):
            shoot_coord.remove(rem[i])
        pygame.display.flip()
    pygame.quit()
