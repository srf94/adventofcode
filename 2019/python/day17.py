from itertools import product
from utils import read_data
from intcode.vm import IntcodeVM


raw = read_data(17)[0].split(",")


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


def get_grid(raw):
    vm = IntcodeVM(raw, mutate_input={0: 1})
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
    scaffolding = {(x, y) for y, row in enumerate(grid) for x, value in enumerate(row) if value == "#"}

    total = 0
    for position in scaffolding:
        for d in range(4):
            if add_direction(position, d) not in scaffolding:
                break
        else:
            total += position[0] * position[1]

    return total


def find_start(grid):
    for (y, row) in enumerate(grid):
        for (x, value) in enumerate(row):
            if value == "^":
                return x, y
    assert False


def find_path_needed(grid):
    path = []
    direction = 2
    loc = find_start(grid)

    while True:
        possible = []
        for d in range(4):
            if d % 2 == direction % 2:
                continue
            new = add_direction(loc, d)
            try:
                if grid[new[1]][new[0]] == "#":
                    possible.append(d)
            except IndexError:
                pass

        if len(possible) != 1:
            break

        new_direction = possible[0]
        assert (new_direction - direction) % 4 in [1, 3]
        turn = "L" if (new_direction - direction) % 4 == 1 else "R"

        count = 0
        while True:
            new = add_direction(loc, new_direction)
            try:
                if grid[new[1]][new[0]] != "#":
                    break
            except IndexError:
                break
            loc = new
            count += 1

        direction = new_direction
        path.append(turn + str(count))

    return path


def get_joined_pattern(pattern):
    return ",".join("{},{}".format(i[0], i[1:]) for i in pattern) + "\n"


def apply_next_pattern(letter, length, coverage, path):
    N = len(path)

    # Get pattern from first non-None value
    start = next(i for i, v in enumerate(coverage) if v is None)
    pattern = path[start : start + length]

    joined_pattern = get_joined_pattern(pattern)
    if 20 < len(joined_pattern):
        return False, False

    all_none = all(i is None for i in coverage[start : start + length])
    if not all_none:
        return False, False

    for i in range(length):
        coverage[start + i] = letter

    loc = 0
    while True:
        if N < loc + length:
            break

        match = path[loc : loc + length] == pattern
        all_none = all(i is None for i in coverage[loc : loc + length])

        if match and all_none:
            for i in range(length):
                coverage[loc + i] = letter
            loc += length
        else:
            loc += 1

    return joined_pattern, coverage


def find_covering_routine(path):
    # Shortest possible step is 'L,4,' so at most 5 can fit into a routine of length 20
    max_len = 5
    letters = ["A", "B", "C"]
    chosen_patterns = None

    # Iterate over all possible patterns until we find a perfect covering - i.e. patterns
    # that are sufficiently short and cover every t
    possible_length_combinations = (range(2, max_len) for _ in range(len(letters)))
    for lengths in product(*possible_length_combinations):
        coverage = [None] * len(path)
        chosen_patterns = []

        for i, letter in enumerate(letters):
            pattern, coverage = apply_next_pattern(letter, lengths[i], coverage, path)
            if not pattern:
                break
            chosen_patterns.append(pattern)
        else:
            if None not in coverage:
                break

    if chosen_patterns is None:
        raise Exception("Could not find solution for part 2")

    loc = 0
    routine = []
    while loc < len(coverage):
        letter = coverage[loc]
        routine.append(letter)
        loc += lengths[letters.index(letter)]
    routine = ",".join(routine) + "\n"

    return routine, chosen_patterns


def part_2(grid):
    path = find_path_needed(grid)
    routine, chosen_patterns = find_covering_routine(path)
    video = "y\n"
    text_input = [ord(i) for i in routine + "".join(chosen_patterns) + video]
    vm = IntcodeVM(raw, mutate_input={0: 2}, input_=text_input)
    output = vm.collect_all_outputs()
    return output[-1]


full_grid = get_grid(raw)


print("Part 1:")
print(part_1(full_grid))


print("Part 2:")
print(part_2(full_grid))
