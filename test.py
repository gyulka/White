
import pygame

if __name__ == '__main__':
    pygame.init()
    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 255), (20, 20), 10)
    pos = (20, 20)
    pygame.display.flip()
    running = True
    flags = {}
    stap = 0
    s = ''
    mandalorian1 = pygame.image.load('mandalorian.png')
    mandalorian1_move1 = pygame.image.load('mandalorian_move1.png')
    mandalorian1_move2 = pygame.image.load('mandalorian_move2.png')
    mandalorian1_shot = pygame.image.load('mandalorian_shot.png')

    mandalorian2_move1 = pygame.image.load('mandalorian_right_move1.png')
    mandalorian2_move2 = pygame.image.load('mandalorian_right_move2.png')
    mandalorian2_shot = pygame.image.load('mandalorian_right_shot.png')

    mandalorian3_move1 = pygame.image.load('mandalorian_left_move1.png')
    mandalorian3_move2 = pygame.image.load('mandalorian_left_move2.png')
    mandalorian3_shot = pygame.image.load('mandalorian_left_shot.png')
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
                if i == pygame.K_w:
                    if pos[1] - 10 >= 20:
                        screen.fill((0, 0, 0))
                        pos = (pos[0], pos[1] - 1)
                if i == pygame.K_a:
                    if pos[0] - 10 >= 20:
                        screen.fill((0, 0, 0))
                        pos = (pos[0] - 1, pos[1])
                        image1 = mandalorian3_move1
                        image2 = mandalorian3_move2
                if i == pygame.K_s:
                    if pos[1] + 10 <= 980:
                        screen.fill((0, 0, 0))
                        pos = (pos[0], pos[1] + 1)
                        image1 = mandalorian1_move1
                        image2 = mandalorian1_move2
                if i == pygame.K_d:
                    if pos[0] + 10 <= 980:
                        screen.fill((0, 0, 0))
                        pos = (pos[0] + 1, pos[1])
                        image1 = mandalorian2_move1
                        image2 = mandalorian2_move2
                if i:
                    stap += 1
                    if stap <= 10:
                        screen.blit(image1, pos)
                    elif stap <= 20:
                        screen.blit(image2, pos)
                    else:
                        screen.blit(image2, pos)
                        stap = 0
        pygame.display.flip()
    pygame.quit()