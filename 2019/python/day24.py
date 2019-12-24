import itertools

raw = """#.#..
.....
.#.#.
.##..
.##.#""".splitlines()
raw = [list(i) for i in raw]


N = 5
midpoint = (N - 1) / 2
squares_1 = list(itertools.product(range(N), range(N)))
squares_2 = [i for i in squares_1 if i != (midpoint, midpoint)]
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def part_1_adjacent(grid, x, y):
    neighbours = [grid.get((x + dx, y - dy), ".") for dx, dy in directions]
    return sum(i == "#" for i in neighbours)


def part_2_adjacent(all_grids, grid_loc, x, y):
    neighbours = []
    grid = all_grids[grid_loc]

    for dx, dy in directions:
        location = (x + dx, y + dy)
        try:
            neighbours.append(grid[location])
            continue
        except KeyError:
            pass

        if location == (midpoint, midpoint):
            # Fails if we are already in the innermost grid and know we
            # will not need to spill into the next grid on this iteration
            try:
                inner = all_grids[grid_loc + 1]
            except:
                continue

            if dy == 0:
                new_x = 0 if dx == 1 else N - 1
                inner_locations = [(new_x, i) for i in range(N)]
            else:
                new_y = 0 if dy == 1 else N - 1
                inner_locations = [(i, new_y) for i in range(N)]
            for l in inner_locations:
                neighbours.append(inner[l])
            continue

        # Similar to innermost case above, fails when we know we do not
        # need to spill over to outer grid on this iteration
        try:
            outer = all_grids[grid_loc - 1]
        except:
            continue
        neighbours.append(outer[(midpoint + dx, midpoint + dy)])

    return sum(i == "#" for i in neighbours)


def update_grid(grid, all_grids=None, grid_loc=None):
    part_1 = bool(all_grids is None)
    squares = squares_1 if part_1 else squares_2

    new = {}
    for (x, y) in squares:
        if part_1:
            adj = part_1_adjacent(grid, x, y)
        else:
            adj = part_2_adjacent(all_grids, grid_loc, x, y)

        current = grid[(x, y)]
        if (adj == 1) or (adj == 2 and current == "."):
            new[(x, y)] = "#"
        else:
            new[(x, y)] = "."

    return new


def draw_grid(grid):
    rows = []
    for y in range(N):
        rows.append("".join(str(grid.get((x, y), "?")) for x in range(N)))
    print("\n".join(rows))


grid_dict = {(x, y): raw[y][x] for (x, y) in squares_1}
seen = set()
while True:
    grid_pattern = tuple(grid_dict[(x, y)] for (y, x) in squares_1)
    if grid_pattern in seen:
        print("Part 1:")
        print(sum(2 ** i for i, value in enumerate(grid_pattern) if value == "#"))
        break

    seen.add(grid_pattern)
    grid_dict = update_grid(grid_dict)


grid_dict = {(x, y): raw[y][x] for (x, y) in squares_2}
grids = {0: grid_dict}
inner_locs = [(midpoint + dx, midpoint + dy) for dx, dy in directions]
outer_locs = [i for i in squares_2 if i[0] in [0, N - 1] or i[1] in [0, N - 1]]


for _ in range(200):
    innermost_grid = grids[max(grids)]
    if any(innermost_grid[i] == "#" for i in inner_locs):
        grids[max(grids) + 1] = {loc: "." for loc in squares_2}

    outermost_grid = grids[min(grids)]
    if any(outermost_grid[i] == "#" for i in outer_locs):
        grids[min(grids) - 1] = {loc: "." for loc in squares_2}

    grids = {loc: update_grid(grids[loc], grids, loc) for loc in grids.keys()}


total_bugs = sum(v == "#" for g in grids.values() for v in g.values())
print("Part 2:")
print(total_bugs)
