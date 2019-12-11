from collections import deque
from utils import read_data
from intcode_vm import run_instructions


raw = read_data(9)[0].split(",")


gen = run_instructions(raw, debug=False)
to_send = [1]
while True:
    next(gen)
    output, terminate = gen.send(deque(to_send))
    if terminate:
        break
    to_send = [output]


print("Part 1:")
print(output)


gen = run_instructions(raw, debug=False)
to_send = [2]
while True:
    next(gen)
    output, terminate = gen.send(deque(to_send))
    if terminate:
        break
    to_send = [output]


print("Part 2:")
print(output)
