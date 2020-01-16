from utils import read_data
from itertools import product
from collections import defaultdict, deque, namedtuple


def add_direction(loc, d):
    x, y = loc
    if d == 0:
        y -= 1
    elif d == 1:
        x += 1
    elif d == 2:
        y += 1
    elif d == 3:
        x -= 1
    else:
        raise Exception(d)
    return x, y


def get_reverse(d):
    return (d + 2) % 4


def parse_gates(grid_dict):
    # Record tuples of:
    # - Letter pair
    # - Adjacent path location
    # - Direction from path to pair
    gate = namedtuple("gate", ("letters", "loc", "dir"))

    gates = []
    for letter_loc, value in grid_dict.items():
        if not value.isalpha():
            continue

        letter = grid_dict[letter_loc]
        for pair_direction in [1, 2]:
            letter_loc_2 = add_direction(letter_loc, pair_direction)
            letter_2 = grid_dict.get(letter_loc_2)
            if letter_2 and letter_2.isalpha():
                break
        else:
            continue

        pair = (letter, letter_2)

        for loc, direction in product([letter_loc, letter_loc_2], range(4)):
            adjacent_loc = add_direction(loc, direction)
            if grid_dict.get(adjacent_loc) == ".":
                gates.append(gate(pair, adjacent_loc, get_reverse(direction)))
                break

    return gates


def pair_gates(gates):
    gate_pairs = defaultdict(list)
    for pair, adjacent_loc, adjacent_direction in gates:
        if pair == ("A", "A"):
            start = adjacent_loc
        elif pair == ("Z", "Z"):
            end = adjacent_loc
        else:
            gate_pairs[pair].append((adjacent_loc, adjacent_direction))

    assert all(len(v) == 2 for v in gate_pairs.values())
    return gate_pairs, start, end


def parse_jumps(gate_pairs, X_len, Y_len):
    jumps = {}
    outer_jumps = set()
    for pair, locs in gate_pairs.items():
        loc_1, d_1 = locs[0]
        loc_2, d_2 = locs[1]
        jumps[(loc_1, d_1)] = loc_2
        jumps[(loc_2, d_2)] = loc_1

        outer_1 = (loc_1[0] < 3 or X_len - 4 < loc_1[0]) or (loc_1[1] < 3 or Y_len - 4 < loc_1[1])
        outer_2 = (loc_2[0] < 3 or X_len - 4 < loc_2[0]) or (loc_2[1] < 3 or Y_len - 4 < loc_2[1])
        assert outer_1 ^ outer_2
        if outer_1:
            outer_jumps.add((loc_1, d_1))
        else:
            outer_jumps.add((loc_2, d_2))

    return jumps, outer_jumps


def find_shortest_path(grid_dict, jumps, outer_jumps, start, end, part):
    assert part in [1, 2]
    part_2 = part == 2

    step = namedtuple("step", ("loc", "d", "level"))
    Q = deque()
    Q.append(step(start, 0, 0))

    SEEN = set()
    LEVEL_CAP = 25
    while True:
        loc, dist, level = Q.popleft()

        if level > LEVEL_CAP:
            continue

        value = grid_dict.get(loc, "#")
        if value != ".":
            continue

        if loc == end and level == 0:
            print("Part {}:".format(part))
            print(dist)
            break

        if (loc, level) in SEEN:
            continue
        SEEN.add((loc, level))

        for d in range(4):
            new_level = level
            new_loc = jumps.get((loc, d))
            if new_loc is None:
                new_loc = add_direction(loc, d)
            elif part_2:
                if (loc, d) in outer_jumps:
                    if level == 0:
                        continue
                    new_level = level - 1
                else:
                    new_level = level + 1

            Q.append(step(new_loc, dist + 1, new_level))


def run_both_parts(raw):
    grid_list = [list(row) for row in raw]
    grid_dict = {(x, y): value for (y, row) in enumerate(grid_list) for (x, value) in enumerate(row)}
    X_len = max(len(i) for i in grid_list)
    Y_len = len(grid_list)

    gates = parse_gates(grid_dict)
    gate_pairs, start, end = pair_gates(gates)
    jumps, outer_jumps = parse_jumps(gate_pairs, X_len, Y_len)

    find_shortest_path(grid_dict, jumps, outer_jumps, start, end, 1)
    find_shortest_path(grid_dict, jumps, outer_jumps, start, end, 2)


run_both_parts(read_data(20))
