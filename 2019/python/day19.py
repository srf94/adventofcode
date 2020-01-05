from utils import read_data
from itertools import product
from collections import deque
from intcode.vm import IntcodeVM


raw = read_data(19)[0].split(",")


def read_square(location):
    return IntcodeVM(raw, input_=deque(location)).run()


print("Part 1:")
print(sum(read_square(pair) for pair in product(range(50), range(50))))


N = 100
loc = (N, 0)
debug = False
pattern = []

while True:
    value = read_square(loc)

    if value == 1:
        bottom_left = (loc[0] - (N - 1), loc[1] + (N - 1))
        value_2 = read_square(bottom_left)
        if value_2 == 1:
            top_left = (bottom_left[0], loc[1])
            if debug:
                print("Solution:")
                print("Top right corner: {}".format(loc))
                print("Bottom left corner: {}".format(bottom_left))
                print("Top left corner: {}".format(top_left))

            print("Part 2:")
            print(top_left[0] * 10000 + top_left[1])
            break

        loc = (loc[0] + 1, loc[1])

    elif value == 0:
        loc = (loc[0], loc[1] + 1)

    else:
        raise Exception()


# CHECK
if debug:
    for x, y in product(range(N), range(N)):
        X, Y = top_left[0] + x, top_left[1] + y
        value = read_square((X, Y))
        if value != 1:
            print("Error when checking - {} has value {}".format((X, Y), value))
            break
    else:
        print("Manual checked full {}x{} square, no errors found".format(N, N))
