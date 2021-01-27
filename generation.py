import csv
import random

import consts
import Pole
BOX = 'box'
RIGHT = '0'
LEFT = '1'
UP = '2'
DOWN = '3'


def gen_map():
    a = consts.a + 0
    b = consts.b + 0
    lis = [[gen_room() for i in range(b)] for i in range(a)]
    lis[a // 2][0] = gen_start()
    i = 0
    j = 2


def gen_room():
    return None

def gen_start():
    with open(f'start_{random.randint(1, 2)}', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        lis = []
        for i in reader:
            lis.append(i)
        return lis
