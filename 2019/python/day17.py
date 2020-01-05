from utils import read_data
from intcode.vm import IntcodeVM


def draw_grid(square):
    print("\n".join("".join(str(i) for i in row) for row in square))


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


def get_reverse(d):
    return {1: 2, 2: 1, 3: 4, 4: 3}[d]


def get_grid(raw, vm):
    flat_grid = vm.collect_all_outputs()

    g, row = [], []
    for value in flat_grid:
        if value == 10:
            g.append(row)
            row = []
        else:
            row.append(chr(value))
    return g


def part_1(grid):
    scaffolding = {
        (x, y) for y, row in enumerate(grid) for x, value in enumerate(row)
        if value == '#'
    }

    total = 0
    for position in scaffolding:
        for d in range(4):
            if add_direction(position, d) not in scaffolding:
                break
        else:
            total += position[0] * position[1]

    print("Part 1:")
    print(total)


raw = read_data(17)[0].split(",")


raw[0] = 1
vm = IntcodeVM(raw, mutate_input={0: 1})
grid = get_grid(raw, vm)

part_1(grid)
