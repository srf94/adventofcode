from utils import read_data
from itertools import product
from collections import defaultdict


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


def distance_between_points(grid_dict, start, target):
    crawled = set()
    path = []
    loc = start
    min_distance = None
    while True:
        for d in range(4):
            new = add_direction(loc, d)
            if grid_dict.get(new, "#") == "#":
                continue

            if new == target:
                distance = len(path) + 1
                if min_distance is None or distance < min_distance:
                    min_distance = distance

            if new not in crawled:
                path.append(new)
                crawled.add(new)
                break
        else:
            if len(path):
                path.pop()
                try:
                    loc = path[-1]
                except IndexError:
                    break
                continue

        loc = path[-1]
    return min_distance


raw_test = """         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z       """.splitlines()


raw_real = read_data(20)
raw = raw_test
raw = raw_real


grid_list = [list(row) for row in raw]
grid_dict = {(x, y): value for (y, row) in enumerate(grid_list) for (x, value) in enumerate(row)}
letter_locs = {(x, y) for (x, y), value in grid_dict.items() if value.isalpha()}


# Record tuples of:
# - Letter pair
# - Adjacent path location
# - Direction from path to pair
letter_tuples = []
for letter_loc in letter_locs:

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
        if grid_dict.get(adjacent_loc) == '.':
            adjacent_direction = get_reverse(direction)
            break

    letter_tuples.append((pair, adjacent_loc, adjacent_direction))


pairings = defaultdict(list)
for pair, adjacent_loc, adjacent_direction in letter_tuples:
    if pair == ('A', 'A'):
        start = adjacent_loc
    elif pair == ('Z', 'Z'):
        end = adjacent_loc
    else:
        pairings[pair].append((adjacent_loc, adjacent_direction))


jumps = {}
for pair, locs in pairings.items():
    loc_1, d_1 = locs[0]
    loc_2, d_2 = locs[1]
    jumps[(loc_1, d_1)] = loc_2
    jumps[(loc_2, d_2)] = loc_1


location = start
path = [(location, 0)]
seen = {location}
min_distance = None
rotate_from = 0


while True:
    for direction in range(rotate_from, 4):
        new = jumps.get((location, direction))
        if new is None:
            new = add_direction(location, direction)
        if grid_dict.get(new) == '.' and new not in seen:
            seen.add(new)
            location = new
            # print('Moved in direction {} to {}'.format(direction, location))
            break
    else:
        if location == start:
            break

        # Reverse back one step
        # print('Reversing back from {} to {}'.format(path[-1][0], path[-2][0]))
        seen.remove(location)
        location = path[-2][0]
        rotate_from = path[-1][1] + 1
        path.pop()
        continue

    path.append((location, direction))
    rotate_from = 0

    if location == end:
        current_distance = len(path) - 1
        if min_distance is None or current_distance < min_distance:
            min_distance = current_distance


print("Part 1:")
print(min_distance)
