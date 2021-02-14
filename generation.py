import random

BOX = 'box'
RIGHT = '2'
LEFT = '4'
UP = '1'
DOWN = '3'


def gen_map():
    a = 5
    b = 5
    lis = [[None for i in range(b + 1)] for i in range(a + 1)]
    lis[a // 2][0] = gen_start()
    i = 1
    j = 2
    from1 = LEFT
    ans = ''
    while i != a or j != 2:
        if i == b:
            ans += DOWN if j > 2 else UP
            lis[j][i] = gen_room(from1, ans[-1])
            from1 = UP if j > 2 else DOWN
        elif j == a:
            ans += RIGHT
            lis[j][i] = gen_room(from1, ans[-1])
            from1 = LEFT
        elif j == 0:
            ans += RIGHT
            lis[j][i] = gen_room(from1, ans[-1])
            from1 = LEFT
        elif i == b:
            ans += DOWN if j > 2 else UP
            lis[j][i] = gen_room(from1, ans[-1])
            from1 = UP if j > 2 else DOWN
        else:
            choises = [k for k in [UP, RIGHT, DOWN] if k != from1]
            ans += random.choice(choises)
            lis[j][i] = gen_room(from1, ans[-1])
            from1 = {RIGHT: LEFT, UP: DOWN, LEFT: RIGHT, DOWN: UP}[ans[-1]]

        if from1 == LEFT:
            i += 1
        elif from1 == UP:
            j -= 1
        elif from1 == DOWN:
            j += 1
    return lis, ans


def gen_room(from1, to1):
    return f'files/levels/{from1}_{to1}_{random.randint(1, 2)}.txt'


def gen_start():
    return f'files/levels/start/start_{random.randint(1, 2)}.txt'


print(gen_map())
