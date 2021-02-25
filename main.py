from collections import defaultdict
from multiprocessing import Pool
from tqdm import tqdm
import math
import pandas as pd
import numpy as np

# pools = Pool(processes=6)
# for ret_code, command in tqdm(pools.imap_unordered(pool_func_train, train), total=len(train)):

def read_input(filename):
    with open(filename,"r") as f:
        lines = [line.replace("\n","") for line in f.readlines()]
        line_1 = lines[0].split(" ")
        duration = int(line_1[0])
        n_intersections = int(line_1[1])
        intersections = list(range(n_intersections))
        n_streets = int(line_1[2])
        n_cars = int(line_1[3])
        bonus_points = int(line_1[4])

        streets = []
        for i in range(1, 1 + n_streets):
            street_data = lines[i].split(" ")
            inter_start = street_data[0]
            inter_end = street_data[1]
            street_name = street_data[2]
            street_duration = street_data[3]
            streets.append((inter_start, inter_end, street_name, street_duration))

        paths = []
        for i in range(1 + n_streets, 1 + n_streets + n_cars):
            path_data = lines[i].split(" ")
            paths.append(path_data[1:])


    return duration, n_intersections, streets, paths, bonus_points




if __name__ == '__main__':

    filename = "data/d.txt"
    print(filename)

    duration, n_intersections, streets, paths, bonus_points = read_input(filename)

    # Get the frequency of the street visits
    street_freq = defaultdict(int)
    for car_path in paths:
        for visited_street in car_path[:-1]:
            street_freq[visited_street] += 1

    light_interval_factor = 20

    intersections = {}

    print("calculating frequency")
    for i in range(n_intersections):
        streets_in = [street[2] for street in streets if int(street[1]) == i]
        intersections[i] = {street: street_freq[street] for street in streets_in if street_freq[street] > 0}

    # Normalize
    print("normalizing")
    for key in intersections.keys():
        values = intersections[key].values()
        if len(values) == 0: continue
        min_visited = min(values)
        for street in intersections[key].keys():
            intersections[key][street] = round(intersections[key][street] / min_visited)

        values = intersections[key].values()
        sum_visited_after = sum(values)
        if sum_visited_after > light_interval_factor:
            for street in intersections[key].keys():
                street_light_interval = round((intersections[key][street] / len(intersections[key])) * light_interval_factor)
                if street_light_interval == 0:
                    intersections[key][street] = None
                else:
                    intersections[key][street] = street_light_interval


    print("printing")
    with open(f"out_{filename.replace('data/','')}", "w+") as f:
        intersections = {key: intersections[key] for key in intersections.keys() if len(intersections[key]) > 0}
        output = f"{len(intersections)}\n"
        for key in intersections.keys():
            intersections[key] = {street: intersections[key][street] for street in intersections[key].keys() if intersections[key][street] is not None}
            if len(intersections[key]) == 0:continue
            output += (f"{key}\n")
            output += (f"{len(intersections[key])}\n")
            for street in intersections[key].keys():
                output +=(f"{street} {intersections[key][street]}\n")


        f.write(output.rstrip())






