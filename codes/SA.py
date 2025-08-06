import os 

import numpy as np
import math, time, random

import json

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "..", "tsp_cases.json")

try:
    with open("tsp_cases.json", "r") as f:
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

def simulated_annealing(distance, city_class, t_range=(1, 100), alpha=0.99, iter_num=1000):
    city_num = len(distance)
    goods_num = len(city_class)
    # t_range = (1,100) creates a tuple with 1 at index 0, and 100 at index 1
    # So initial temp becomes 100
    t = t_range[1]  # Initial temperature

    # Generate random initial solution
    new_solution = [x[random.randrange(len(x))] for x in city_class]
    random.shuffle(new_solution)
    new_value = cal_cost(distance, new_solution, goods_num)

    current_solution = new_solution.copy()
    current_value = [new_value]

    best_solution = new_solution.copy()
    bestvalue = new_value
    best_value = [bestvalue]

    while t > t_range[0]:
        for _ in range(iter_num):
            candidate = new_solution.copy()
            seed = np.random.rand()

            if 0.3 < seed < 0.7:
                while True:
                    goods = random.randrange(goods_num)
                    if len(city_class[goods]) > 1:
                        break
                for index, city in enumerate(city_class[goods]):
                    if city in candidate:
                        loc = candidate.index(city)
                        while True:
                            tmp = random.randrange(len(city_class[goods]))
                            if tmp != index:
                                break
                        candidate[loc] = city_class[goods][tmp]

            elif seed > 0.7:
                while True:
                    loc1 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    loc2 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    if loc1 != loc2:
                        break
                candidate[loc1], candidate[loc2] = candidate[loc2], candidate[loc1]

            else:
                while True:
                    #What if I dont have >= 3 clusters --> ERROR?????
                    loc1 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    loc2 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    loc3 = int(np.ceil(np.random.rand() * (goods_num - 1)))
                    if len(set([loc1, loc2, loc3])) == 3:
                        break
                loc1, loc2, loc3 = sorted([loc1, loc2, loc3])
                tmplist = candidate[loc1:loc2].copy()
                candidate[loc1:loc3 - loc2 + 1 + loc1] = candidate[loc2:loc3 + 1].copy()
                candidate[loc3 - loc2 + 1 + loc1:loc3 + 1] = tmplist.copy()

            candidate_value = cal_cost(distance, candidate, goods_num)
            delta = candidate_value - new_value

            if delta < 0 or np.random.rand() < math.exp(-delta / t):
                new_solution = candidate
                new_value = candidate_value

                if new_value < bestvalue:
                    bestvalue = new_value
                    best_solution = new_solution.copy()

            current_value.append(new_value)
            best_value.append(bestvalue)

        t *= alpha  # Cooling

    return best_solution, bestvalue, best_value

def main():
    for i, (city_position, goods_class, city_class) in enumerate(extendTSP_cases):
        print(f"\n=== Running Simulated Annealing on Test Case {i + 1} ===")
        # Cities is stored in a 2D Array, split by good type
        # Goods is a 1D Array of goods corresponding to each class index
        # So len(goods_class) = Number of cities & len(city_class) = Number of goods
        print(f"\nNumber of goods = {len(city_class)}")
        print(f"\nNumber of cities = {len(goods_class)}")
        # Commented lines for printing the classes & city positions
        # print(f"City positions:\n{city_position}")
        # print(f"Goods class:\n{goods_class}")
        # print(f"City class:\n{city_class}")

        distance = record_distance(city_position)

        start_time = time.time()
        best_path, best_cost, _ = simulated_annealing(distance, city_class)
        end_time = time.time()

        print(f"Test Case {i + 1}: Best cost = {best_cost:.2f}")
        print(f"Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
