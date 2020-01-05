import itertools
from collections import deque
from utils import read_data
from intcode.vm import IntcodeVM


raw = read_data(7)[0].split(",")


outputs = []
for sequence in itertools.permutations(range(5)):
    output = 0
    for phase in sequence:
        output = IntcodeVM(raw, input_=deque([phase, output])).run()
    outputs.append(output)


print("Part 1:")
print(max(outputs))


outputs = []
for sequence in itertools.permutations(range(5, 10)):
    output = 0

    amplifiers = {phase: IntcodeVM(raw) for phase in sequence}

    for loc, phase in enumerate(itertools.cycle(sequence)):
        if loc < 5:
            data_input = deque([phase, output])
        else:
            data_input = deque([output])

        vm = amplifiers[phase]
        output = vm.run(data_input)
        if output is None:
            outputs.append(vm.input.popleft())
            break


print("Part 2:")
print(max(outputs))
