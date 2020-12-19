import pygame

if __name__ == '__main__':
    pygame.init()
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
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                flags[event.key] = True
            if event.type == pygame.KEYUP:
                flags[event.key] = False
        screen.fill((0, 0, 0))
        screen.blit(mandalorian1, pos)
        for i in flags:
            if flags[i]:
                image1 = mandalorian1_move1
                image2 = mandalorian1_move2
                check_and_break = False
                if i == pygame.K_w:
                    if pos[1] - 1 >= 1:
                        screen.fill((0, 0, 0))
                        pos = (pos[0], pos[1] - 1)
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
        pygame.display.flip()
    pygame.quit()