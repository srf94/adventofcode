import itertools
import numpy as np
from utils import read_data


class Planet:
    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = np.zeros(self.position.shape)

    def energy(self):
        kin = np.abs(self.velocity).sum()
        pot = np.abs(self.position).sum()
        return kin * pot


def input_to_tuple(string):
    return tuple(int(i.split("=")[1]) for i in string.strip("<>").split(","))


def run_step(planets):
    for p1, p2 in itertools.combinations(planets, 2):
        velocity_diff = p2.position - p1.position

        velocity_delta = np.zeros(velocity_diff.shape)
        velocity_delta[velocity_diff > 0] = 1
        velocity_delta[velocity_diff < 0] = -1

        p1.velocity = p1.velocity + velocity_delta
        p2.velocity = p2.velocity - velocity_delta

    for p in planets:
        p.position = p.position + p.velocity


raw = read_data(12)
planets_3d = [Planet(input_to_tuple(s)) for s in raw]


num_steps = 1000
for t in xrange(num_steps):
    run_step(planets_3d)


print("Part 1:")
print(int(sum(p.energy() for p in planets_3d)))


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(nums):
    a = nums.pop()
    if len(nums) == 1:
        b = nums.pop()
    else:
        b = lcm(nums)
    return a * b / gcd(a, b)


steps_to_repeat = []
for index in range(3):
    planets_1d = [Planet(input_to_tuple(s)[index]) for s in raw]

    t = 0
    seen_states = set()

    while True:
        run_step(planets_1d)
        state = tuple((i.position.tolist(), i.velocity.tolist()) for i in planets_1d)
        if state in seen_states:
            break

        t += 1
        seen_states.add(state)

    steps_to_repeat.append(t)


print("Part 2:")
print(lcm(steps_to_repeat))
