from utils import read_data
from intcode_vm import IntcodeVM


def draw_grid(g):
    x_dim = [min(i for i, _ in grid), max(i for i, _ in grid)]
    y_dim = [min(j for _, j in grid), max(j for _, j in grid)]

    square = [[" "] * (1 + x_dim[1] - x_dim[0]) for _ in range(1 + y_dim[1] - y_dim[0])]

    for (x, y), v in g.items():
        char = "O" if v == 2 else ("." if v == 0 else " ")
        square[y - y_dim[0]][x - x_dim[0]] = char

    square[-y_dim[0]][-x_dim[0]] = "S"

    print("\n".join("".join(str(i) for i in row) for row in reversed(square)))


def add_direction(loc, d):
    x, y = loc
    if 2 < d:
        y += -1 if d == 3 else 1
    else:
        x += -1 if d == 2 else 1
    return x, y


def get_reverse(d):
    return {1: 2, 2: 1, 3: 4, 4: 3}[d]


raw = read_data(15)[0].split(",")
vm = IntcodeVM(raw)


oxygen_location = None
location = (0, 0)
grid = {location: 1}
path = [(location, 0)]


while True:
    # If any adjacent node not visited - visit it
    # Otherwise, step back along the path until we can
    # Finish when at 0,0 and all paths have been visited

    for direction in range(1, 5):
        new = add_direction(location, direction)
        if new not in grid:
            break
    else:
        if location == (0, 0):
            break

        # Reverse back one step
        location = path[-2][0]
        direction = path[-1][1]
        vm.run(get_reverse(direction))
        path.pop()
        continue

    output = vm.run(direction)
    grid[new] = output

    if output in [1, 2]:
        location = new
        path.append((location, direction))

    if output == 2:
        oxygen_location = location
        print("Part 1:")
        print(len(path) - 1)


location = oxygen_location
path = [(location, None)]
seen = {location}


max_distance = 0
while True:
    for direction in range(1, 5):
        new = add_direction(location, direction)
        if grid.get(new, 0) == 1 and new not in seen:
            seen.add(new)
            location = new
            break
    else:
        if location == (0, 0):
            break

        # Reverse back one step
        location = path[-2][0]
        path.pop()
        continue

    path.append((location, direction))
    current_distance = len(path) - 1
    if max_distance < current_distance:
        max_distance = current_distance


print("Part 2:")
print(max_distance)
