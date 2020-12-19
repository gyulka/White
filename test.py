import pygame


def move():
    global stap, pos
    for i in flags:
        if flags[i]:
            if i == pygame.K_w:
                if pos[1] - 10 >= 20:
                    screen.fill((0, 0, 0))
                    pos = (pos[0], pos[1] - 1)
                    stap += 1
                    if stap % 2 == 0:
                        screen.blit(mandalorian1_move1, pos)
                    else:
                        screen.blit(mandalorian1_move2, pos)
            if i == pygame.K_a:
                if pos[0] - 10 >= 20:
                    screen.fill((0, 0, 0))
                    pos = (pos[0] - 1, pos[1])
                    stap += 1
                    if stap % 2 == 0:
                        screen.blit(mandalorian1_move1, pos)
                    else:
                        screen.blit(mandalorian1_move2, pos)
            if i == pygame.K_s:
                if pos[1] + 10 <= 980:
                    screen.fill((0, 0, 0))
                    pos = (pos[0], pos[1] + 1)
                    stap += 1
                    if stap % 2 == 0:
                        screen.blit(mandalorian1_move1, pos)
                    else:
                        screen.blit(mandalorian1_move2, pos)
            if i == pygame.K_d:
                if pos[0] + 10 <= 980:
                    screen.fill((0, 0, 0))
                    pos = (pos[0] + 1, pos[1])
                    stap += 1
                    if stap % 2 == 0:
                        screen.blit(mandalorian1_move1, pos)
                    else:
                        screen.blit(mandalorian1_move2, pos)


if __name__ == '__main__':
    pygame.init()
    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    pos = (20, 20)
    pygame.display.flip()
    running = True
    flags = {}
    stap = 0
    s = ''
    mandalorian1 = pygame.image.load('files/textures/main_charachter_1/mandalorian.png')
    mandalorian1_move1 = pygame.image.load('files/textures/main_charachter_1/mandalorian_move1.png')
    mandalorian1_move2 = pygame.image.load('files/textures/main_charachter_1/mandalorian_move2.png')
    mandalorian1_shot = pygame.image.load('files/textures/main_charachter_1/mandalorian_shot.png')
    while running:
        screen.fill((0, 0, 0))
        screen.blit(mandalorian1, pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                flags[event.key] = True
                print(1)
            if event.type == pygame.KEYUP:
                flags[event.key] = False
        move()
        pygame.display.flip()
    pygame.quit()
