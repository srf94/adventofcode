import itertools
from collections import deque
from utils import read_data
from intcode_vm import run_instructions


raw = read_data(7)[0].split(",")


outputs = []
for sequence in itertools.permutations(range(5)):
    output = 0
    for phase in sequence:
        gen = run_instructions(raw)
        gen.next()
        output, _ = gen.send(deque([phase, output]))
    outputs.append(output)


print("Part 1:")
print(max(outputs))


sequence = list(range(5, 10))
outputs = []
for sequence in itertools.permutations(range(5, 10)):
    output = 0

    generators = {}
    for phase in sequence:
        gen = run_instructions(raw)
        gen.next()
        generators[phase] = gen

    for loc, phase in enumerate(itertools.cycle(sequence)):
        if loc < 5:
            data_input = deque([phase, output])
        else:
            data_input = deque([output])

        gen = generators[phase]
        output, ended = gen.send(data_input)
        if ended:
            output = data_input.popleft()
            break
        gen.next()
    outputs.append(output)


print("Part 2:")
print(max(outputs))
