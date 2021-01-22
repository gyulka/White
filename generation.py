import csv
import random

BOX = 'box'
RIGHT = '0'
LEFT = '1'
UP = '2'
DOWN = '3'


def gen_start():
    with open(f'start_{random.randint(1, 2)}', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        lis = []
        for i in reader:
            lis.append(i)
        return lis
