import random

# from data.units.consts import LEFT,RIGHT,UP,DOWN


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
            ans += UP if j > 2 else DOWN
            lis[j][i] = gen_room(from1, ans[-1])
            from1 = DOWN if j > 2 else UP
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
            j += 1
        elif from1 == DOWN:
            j -= 1
    if lis[1][-1] is not None:
        lis[2][-1] = gen_room(UP, 0)
    elif lis[3][-1]:
        lis[2][-1] = gen_room(DOWN, 0)
    else:
        lis[2][-1] = gen_room(LEFT, 0)
    return lis, ans


def gen_room(from1, to1):
    if (from1 == '3' and to1 == '1') or (from1 == '1' and to1 == '3'):
        return f'data/levels/{3}_{1}_{1}.txt'
    return f'data/levels/{from1}_{to1}_{1}.txt'


def gen_start():
    return f'data/levels/0_{2}_1.txt'
