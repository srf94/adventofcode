from utils import read_data
from collections import deque, namedtuple


def add_direction(loc, d):
    x, y = loc
    if d == 0:
        y += 1
    elif d == 1:
        x += 1
    elif d == 2:
        y -= 1
    elif d == 3:
        x -= 1
    else:
        raise Exception(d)
    return x, y


def get_start_locations(grid):
    return [(x, y) for (x, y), value in grid.items() if value == "@"]


raw = read_data(18)


grid = {(x, y): value for (y, row) in enumerate(raw) for (x, value) in enumerate(list(row))}
start = get_start_locations(grid)[0]
all_nodes = {i for i in grid.values() if i.islower()}


step = namedtuple("step", ("loc", "seen", "d"))
Q = deque()
Q.append(step(start, {}, 0))
SEEN = set()


while True:
    loc, seen, dist = Q.popleft()

    value = grid.get(loc, "#")
    if value == "#":
        continue

    if value.isupper() and value.lower() not in seen:
        continue

    key = (loc, tuple(sorted(seen)))
    if key in SEEN:
        continue
    SEEN.add(key)

    if value.islower():
        seen = {i for i in seen}
        seen.add(value)
        if seen == all_nodes:
            print("Part 1:")
            print(dist)
            break

    for d in range(4):
        new_loc = add_direction(loc, d)
        Q.append(step(new_loc, seen, dist + 1))
