import math
from utils import read_data
from itertools import product
from collections import defaultdict


def gcd(a, b):
    while b:
        a, b = b, a%b
    return a


def get_direction(pos_1, pos_2):
    x = pos_2[0] - pos_1[0]
    y = pos_2[1] - pos_1[1]
    gcd_ = abs(gcd(x, y))
    return x/gcd_, y/gcd_


def get_angle(x, y):
    angle = math.atan2(x, -y)
    if angle < 0:
        angle += 2*math.pi
    return angle


def get_distance(pos_1, pos_2):
    return math.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)


data = read_data(10)
asteroids = {(x, y) for x, y in product(range(len(data[0])), range(len(data))) if data[y][x] == '#'}


visible = {}
for asteroid in asteroids:
    visible[asteroid] = len({get_direction(asteroid, a) for a in asteroids if a != asteroid})


chosen_asteroid = max(visible, key=visible.get)
visible_asteroids = visible[chosen_asteroid]
print("Part 1:")
print(visible_asteroids)


direction_groups = defaultdict(list)
for asteroid in asteroids:
    if chosen_asteroid == asteroid:
        continue

    vector = get_direction(chosen_asteroid, asteroid)
    direction_groups[vector].append(asteroid)


ordered_vectors = sorted([
    vector for vector in direction_groups.keys()
], key=lambda x: get_angle(*x))


count = 0
pointer = 0
while True:
    vector = ordered_vectors[pointer]
    vector_asteroids = direction_groups[vector]
    if not vector_asteroids:
        pointer += 1
        continue

    distances = {get_distance(chosen_asteroid, a): a for a in vector_asteroids}
    asteroid = distances[min(distances)]

    vector_asteroids.pop(vector_asteroids.index(asteroid))
    pointer += 1
    count += 1

    if count == 200:
        print("Part 2:")
        print(asteroid[0] * 100 + asteroid[1])
        break

    if pointer >= len(ordered_vectors):
        pointer = 0
