import numpy as np
from collections import defaultdict

with open('../input/day24.txt', 'r') as f:
    data = f.read().splitlines()

def step(remaining, used, last=None, part_1=True):
    if not last:
        last = 0

    options = [i for i in remaining if last in i]

    if not options:
        return 0, 0

    max_sum = 0
    max_len = len(used)
    for option in options:
        new_remaining = [i for i in remaining if i != option]
        new_used = [i for i in used] + [option]
        new_last = option[1] if option[0] == last else option[0]

        sum_, len_ = step(new_remaining, new_used, last=new_last, part_1=part_1)
        sum_ += option[0] + option[1]

        if part_1:
            if sum_ > max_sum:
                max_sum = sum_

        else:
            new_len = len(used) + len_
            if new_len > max_len:
                max_sum = sum_
                max_len = new_len
            elif new_len == max_len and sum_ > max_sum:
                max_sum = sum_

    return max_sum, max_len


components = [i.split("/") for i in data]
components = [(int(i), int(j)) for i, j in components]

print "Part 1: %s" % step(components, [], part_1=True)[0]
print "Part 2: %s" % step(components, [], part_1=False)[0]
