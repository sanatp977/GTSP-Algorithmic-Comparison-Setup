# -*- coding:utf-8 -*-
import random
import math
import numpy as np
import matplotlib.pyplot as plt

extendTSP_cases = []

def classify_city(goods_class):
    goods_num = len(set(goods_class))
    city_class = [[] for _ in range(goods_num)]
    for idx, g in enumerate(goods_class):
        city_class[g].append(idx)
    return city_class

def gen_case(city_num, goods_num, x_range=100, y_range=100):
    city_position = set()
    while len(city_position) < city_num:
        city_position.add((random.randrange(x_range), random.randrange(y_range)))
    city_position = list(city_position)

    goods_class = list(range(goods_num))
    while len(goods_class) < city_num:
        goods_class.append(random.randrange(goods_num))
    random.shuffle(goods_class)

    city_class = classify_city(goods_class)
    return city_position, goods_class, city_class

# Your existing 5 test cases (unchanged)
''' RAND_CASES = [
    [(21, 30), (27, 46), (80, 59), (59, 55), (40, 75), (39, 35), (53, 65), (41, 53), (40, 76), (15, 52)],
    [(81, 34), (59, 57), (41, 19), (66, 76), (33, 41), (94, 66), (55, 74), (53, 49), (91, 55), (35, 83)],
    [(90, 45), (56, 27), (55, 65), (16, 26), (92, 69), (80, 94), (19, 61), (63, 20), (94, 41), (52, 77)],
    [(49, 50), (28, 43), (57, 98), (91, 42), (32, 67), (96, 88), (38, 90), (90, 34), (93, 76), (63, 63)],
    [(58, 84), (18, 18), (82, 23), (75, 43), (21, 32), (35, 53), (96, 36), (51, 29), (36, 66), (93, 30)],
]

GOODS_CASES = [
    [0, 1, 2, 3, 4, 0, 1, 2, 3, 4],
    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
    [0, 1, 2, 3, 4, 0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4, 0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4, 0, 1, 2, 3, 4],
]

for i in range(5):
    city_position = RAND_CASES[i]
    goods_class = GOODS_CASES[i]
    city_class = classify_city(goods_class)
    extendTSP_cases.append((city_position, goods_class, city_class))

'''

# 🔁 Add 16 new generated test cases
for goods in (5, 10, 15, 20):
    for city_num in (10, 15, 20, 25):
        if goods <= city_num:
         extendTSP_cases.append(gen_case(city_num, goods))

def record_distance(city_position):
    city_num = len(city_position)
    distance = [[0.0 for _ in range(city_num)] for _ in range(city_num)]
    for i in range(city_num):
        for j in range(i + 1, city_num):
            dis = math.sqrt(
                (city_position[i][0] - city_position[j][0]) ** 2 +
                (city_position[i][1] - city_position[j][1]) ** 2
            )
            distance[i][j] = dis
            distance[j][i] = dis
    return distance

def cal_cost(distance, path, goods_num):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += distance[path[i]][path[i+1]]
    total_cost += distance[path[-1]][path[0]]
    return total_cost

def drawPath(city_position, best_path, title='Best Path'):
    x = [city_position[i][0] for i in best_path]
    y = [city_position[i][1] for i in best_path]
    plt.plot(x, y, marker='o')
    plt.title(title)
    for i, (x_, y_) in enumerate(city_position):
        plt.text(x_, y_, str(i))
    plt.show()

print(extendTSP_cases)