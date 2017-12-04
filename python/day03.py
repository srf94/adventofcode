import numpy as np


def get_position(n):
    if n == 1:
        return [0, 0]

    # Use square numbers to find initial position
    i = 3
    while True:
        if i ** 2 > n:
            i -= 2
            break
        i += 2

    number = i ** 2
    position = np.array([(i-1)/2, -(i-1)/2])
    side_length = i + 1
    directions = [np.array(i) for i in (1, 0), (0, 1), (-1, 0), (0, -1), (1, 0)]
    side_counts = [1, side_length - 1, side_length, side_length, side_length]

    for direction, side_count in zip(directions, side_counts):
        for _ in range(side_count):
            if number == n:
                return position
            position += direction
            number += 1


def get_position_values(target_value):
    positions = {(0, 0): 1}

    number = 1
    side_length = 0
    position = np.array([0, 0])
    adjacent_map = [np.array(i) for i in (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    directions = [np.array(i) for i in (1, 0), (0, 1), (-1, 0), (0, -1), (1, 0)]

    while True:
        side_length += 2
        side_counts = [1, side_length - 1, side_length, side_length, side_length]

        for direction, side_count in zip(directions, side_counts):
            for _ in range(side_count):
                position += direction
                number += 1

                new_value = sum(positions.get(tuple(position + loc), 0) for loc in adjacent_map)
                positions[tuple(position)] = new_value

                if new_value > target_value:
                    return new_value

N = 368078
print "Part 1: %s" % sum(abs(int(i)) for i in get_position(N))
print "Part 2: %s" % get_position_values(N)
