import os
import numpy as np
import matplotlib.pyplot as plt
import random
import time
# from extendTSP import *

import json

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "..", "tsp_cases.json")

try:
    with open(json_path, "r") as f:
        extendTSP_cases = json.load(f)
except FileNotFoundError:
    print("Error: 'tsp_cases.json' not found. Please ensure the file is in the correct directory.")
    exit(1)
except json.JSONDecodeError:
    print("Error: 'tsp_cases.json' is not a valid JSON file.")
    exit(1)

for i, (city_position, goods_class, city_class) in enumerate(extendTSP_cases):
    print(f"Test Case {i + 1}")
    print("City positions:", city_position)
    print("Goods:", goods_class)
    print("Class:", city_class)
    print()

import math

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

def cal_popvalue(pop, distance, goods_num):
    return [cal_cost(distance, p, goods_num) for p in pop]

def selection(pop, fitvalue, popsize):
    newpop = [[] for _ in range(popsize)]
    totalfit = sum(fitvalue)
    p_fitvalue = np.cumsum([v / totalfit for v in fitvalue])
    ms = np.sort(np.random.rand(popsize, 1))
    fitin = newin = 0
    while newin < popsize:
        if ms[newin] < p_fitvalue[fitin]:
            newpop[newin] = pop[fitin].copy()
            newin += 1
        else:
            fitin += 1
    return newpop

def rm_repeat(pop, city_class):
    repeat_status = False
    for item in city_class:
        if len(item) > 1:
            repeat_status = False
            for city in item:
                if city in pop:
                    if not repeat_status:
                        repeat_status = True
                    else:
                        pop.remove(city)
    return pop

def cross_pop(pop1, pop2, goods_num, city_class):
    index1 = np.random.randint(0, goods_num - 1)
    index2 = np.random.randint(index1, goods_num - 1)
    tempGene = pop2[index1:index2]
    newGene = []
    counter = 0
    for city in pop1:
        if counter == index1:
            newGene.extend(tempGene)
        if city not in tempGene:
            newGene.append(city)
        counter += 1
    return rm_repeat(newGene, city_class)

def crossover(pop, pc, popsize, goods_num, distance, city_class):
    newpop = [[] for _ in range(popsize)]
    for i in range(0, popsize, 2):
        newpop[i] = pop[i].copy()
        if i != popsize - 1:
            if np.random.rand() < pc:
                newpop[i] = cross_pop(pop[i], pop[i + 1], goods_num, city_class)
                newpop[i + 1] = cross_pop(pop[i + 1], pop[i], goods_num, city_class)
                if cal_cost(distance, newpop[i], goods_num) > cal_cost(distance, pop[i], goods_num):
                    newpop[i] = pop[i]
            else:
                newpop[i + 1] = pop[i + 1]
    return newpop

def mutation(pop, pm, popsize, goods_num, city_class, distance):
    newpop = [[] for _ in range(popsize)]
    for i in range(popsize):
        newpop[i] = pop[i].copy()
        if random.random() < pm:
            seed = np.random.rand()
            if 0.3 < seed < 0.7:
                while True:
                    goods = random.randrange(goods_num)
                    if len(city_class[goods]) > 1:
                        break
                for index, city in enumerate(city_class[goods]):
                    if city in newpop[i]:
                        loc = newpop[i].index(city)
                        while True:
                            tmp = random.randrange(len(city_class[goods]))
                            if tmp != index:
                                break
                        newpop[i][loc] = city_class[goods][tmp]

            elif seed > 0.7:
                while True:
                    loc1 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    loc2 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    if loc1 != loc2:
                        break
                newpop[i][loc1], newpop[i][loc2] = newpop[i][loc2], newpop[i][loc1]

            else:
                while True:
                    loc1 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    loc2 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    loc3 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    if len(set([loc1, loc2, loc3])) == 3:
                        break
                loc1, loc2, loc3 = sorted([loc1, loc2, loc3])
                tmplist = newpop[i][loc1:loc2].copy()
                newpop[i][loc1:loc3 - loc2 + 1 + loc1] = newpop[i][loc2:loc3 + 1].copy()
                newpop[i][loc3 - loc2 + 1 + loc1:loc3 + 1] = tmplist.copy()

            if cal_cost(distance, newpop[i], goods_num) > cal_cost(distance, pop[i], goods_num):
                newpop[i] = pop[i]
    return newpop

def best(pop, value):
    bestindividual = pop[0]
    bestvalue = value[0]
    for i in range(len(pop)):
        if value[i] < bestvalue:
            bestindividual = pop[i]
            bestvalue = value[i]
    return [bestindividual, bestvalue]

def run_ga(distance, city_class, iter_num=10000, pc=0.1, pm=0.8):
    city_num = len(distance)
    goods_num = len(city_class)
    popsize = city_num
    pop = []
    while len(pop) < popsize:
        current_solution = [x[random.randrange(len(x))] for x in city_class]
        random.shuffle(current_solution)
        pop.append(current_solution)

    pop_value = cal_popvalue(pop, distance, goods_num)
    bestindividual, bestvalue = best(pop, pop_value)
    current_value = [bestvalue]
    best_value = [bestvalue]
    best_solution = bestindividual

    for _ in range(iter_num):
        fitvalue = [1 / v for v in pop_value]
        newpop = selection(pop, fitvalue, popsize)
        newpop = crossover(newpop, pc, popsize, goods_num, distance, city_class)
        newpop = mutation(newpop, pm, popsize, goods_num, city_class, distance)
        pop = newpop

        pop_value = cal_popvalue(pop, distance, goods_num)
        bestindividual, bestvalue = best(pop, pop_value)
        current_value.append(bestvalue)
        if bestvalue < best_value[-1]:
            best_solution = bestindividual
            best_value.append(bestvalue)
        else:
            best_value.append(best_value[-1])

    return best_solution, best_value[-1], best_value

def main():
    for i, (city_position, goods_class, city_class) in enumerate(extendTSP_cases):
        print(f"\n=== Running GA on Test Case {i + 1} ===")
        # Cities is stored in a 2D Array, split by good type
        # Goods is a 1D Array of goods corresponding to each class index
        # So len(goods_class) = Number of cities & len(city_class) = Number of goods
        print(f"\nNumber of goods = {len(city_class)}")
        print(f"\nNumber of cities = {len(goods_class)}")
        print(f"City positions:\n{city_position}")
        print(f"Goods class:\n{goods_class}")
        print(f"City class:\n{city_class}")

        distance = record_distance(city_position)

        start_time = time.time()
        best_path, best_cost, _ = run_ga(distance, city_class)
        end_time = time.time()

        print(f"Test Case {i + 1}: Best cost = {best_cost:.2f}")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
        print("\n\n\n\n")

if __name__ == "__main__":
    main()


'''
# -*- coding:utf-8 -*-
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from extendTSP import extendTSP_cases, record_distance, cal_cost

def selection(pop, fitvalue, popsize):
    total_fit = sum(fitvalue)
    if total_fit == 0:
        probs = [1/popsize] * popsize
    else:
        probs = [f / total_fit for f in fitvalue]
    indices = np.random.choice(range(popsize), size=popsize, replace=True, p=probs)
    newpop = [pop[i][:] for i in indices]
    return newpop

def crossover(pop, pc):
    for i in range(0, len(pop) - 1, 2):
        if random.random() < pc:
            c1 = pop[i]
            c2 = pop[i+1]
            point = random.randint(1, len(c1) - 2)
            temp1 = c1[:point] + [x for x in c2 if x not in c1[:point]]
            temp2 = c2[:point] + [x for x in c1 if x not in c2[:point]]
            pop[i] = temp1
            pop[i+1] = temp2
    return pop

def mutation(pop, pm):
    for i in range(len(pop)):
        if random.random() < pm:
            p1 = random.randint(0, len(pop[i]) - 1)
            p2 = random.randint(0, len(pop[i]) - 1)
            pop[i][p1], pop[i][p2] = pop[i][p2], pop[i][p1]
    return pop

def generate_initial_population(city_class, distance, popsize):
    population = []
    for _ in range(popsize):
        path = []
        for cls in city_class:
            path.append(random.choice(cls))
        remaining = [i for i in range(len(distance)) if i not in path]
        random.shuffle(remaining)
        path += remaining
        population.append(path)
    return population

def fitness(pop, distance, goods_num):
    return [1.0 / (cal_cost(distance, ind, goods_num) + 1e-6) for ind in pop]

def run_ga(distance, city_class, popsize=50, generations=200, pc=0.8, pm=0.1):
    goods_num = len(city_class)
    population = generate_initial_population(city_class, distance, popsize)
    best_cost = float('inf')
    best_path = []

    for gen in range(generations):
        fit_value = fitness(population, distance, goods_num)
        population = selection(pop=population, fitvalue=fit_value, popsize=popsize)
        population = crossover(population, pc)
        population = mutation(population, pm)

        for ind in population:
            cost = cal_cost(distance, ind, goods_num)
            if cost < best_cost:
                best_cost = cost
                best_path = ind[:]

    return best_path, best_cost, population

def main():
    for i, (city_position, goods_class, city_class) in enumerate(extendTSP_cases):
        print(f"Running GA on test case {i + 1} ...")
        distance = record_distance(city_position)
        best_path, best_cost, _ = run_ga(distance, city_class)
        print(f"Test case {i + 1}: Best cost = {best_cost:.2f}")
        # Optional: drawPath(city_position, best_path)

if __name__ == "__main__":
    main()
'''