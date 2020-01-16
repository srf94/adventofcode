from utils import read_data
from collections import defaultdict


raw = read_data(3)
w1 = raw[0].split(",")
w2 = raw[1].split(",")


def draw_wire_path(wire_path, move_input):
    pos = [0, 0]
    steps = 0
    steps_dict = {}

    for move in move_input:
        direction = move[0]
        distance = int(move[1:])

        dir_loc = 0 if direction in ["L", "R"] else 1
        dir_val = 1 if direction in ["R", "U"] else -1

        for _ in range(distance):
            pos[dir_loc] += dir_val
            wire_path[tuple(pos)] += 1

            steps += 1
            steps_dict[tuple(pos)] = steps_dict.get(tuple(pos), steps)

    # Ignore cases where a wire crosses itself
    wire_path = {p: 1 for p in wire_path.keys()}

    return wire_path, steps_dict


wires_1, steps_1 = draw_wire_path(defaultdict(int), w1)
wires_2, steps_2 = draw_wire_path(defaultdict(int), w2)

crossover = set(wires_1).intersection(set(wires_2))

print("Part 1:")
cross = [abs(x) + abs(y) for x, y in crossover]
print(min(cross))

print("Part 2:")
print(min([steps_1[i] + steps_2[i] for i in crossover]))
