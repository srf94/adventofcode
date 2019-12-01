import numpy as np
from collections import defaultdict

with open('../input/day25.txt', 'r') as f:
    data = f.read().splitlines()

state = "A"
loop_count = 12656374

tape = defaultdict(int)
loc = 0

for i in xrange(loop_count):

    if state == "A":
        if tape[loc] == 0:
            tape[loc] = 1
            loc += 1
            state = "B"
        elif tape[loc] == 1:
            tape[loc] = 0
            loc -= 1
            state = "C"

    elif state == "B":
        if tape[loc] == 0:
            tape[loc] = 1
            loc -= 1
            state = "A"
        elif tape[loc] == 1:
            tape[loc] = 1
            loc -= 1
            state = "D"

    elif state == "C":
        if tape[loc] == 0:
            tape[loc] = 1
            loc += 1
            state = "D"
        elif tape[loc] == 1:
            tape[loc] = 0
            loc += 1
            state = "C"

    elif state == "D":
        if tape[loc] == 0:
            tape[loc] = 0
            loc -= 1
            state = "B"
        elif tape[loc] == 1:
            tape[loc] = 0
            loc += 1
            state = "E"

    elif state == "E":
        if tape[loc] == 0:
            tape[loc] = 1
            loc += 1
            state = "C"
        elif tape[loc] == 1:
            tape[loc] = 1
            loc -= 1
            state = "F"

    elif state == "F":
        if tape[loc] == 0:
            tape[loc] = 1
            loc -= 1
            state = "E"
        elif tape[loc] == 1:
            tape[loc] = 1
            loc += 1
            state = "A"


print sum(tape.values())

"""
"""
print "Part 1: %s" % step(components, [], part_1=True)[0]
print "Part 2: %s" % step(components, [], part_1=False)[0]
