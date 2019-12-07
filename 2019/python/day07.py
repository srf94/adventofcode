import itertools
from collections import deque
from utils import read_data


raw = read_data(7)
raw = raw[0].split(",")


def read(data, pointer, increment, mode):
    loc = pointer + increment
    value = data[loc]
    if mode:
        return value
    return data[value]


def write(data, pointer, increment, value):
    loc = pointer + increment
    data[data[loc]] = value


def run_instructions(raw_data):
    data_input = yield
    pointer = 0
    program_output = "No output given!"
    import copy
    data = [int(i) for i in copy.deepcopy(raw_data)]

    while True:
        instruction = data[pointer]
        opcode = instruction % 100

        mode_A = bool((instruction // 100) % 10)
        mode_B = bool((instruction // 1000) % 10)
        mode_C = bool((instruction // 10000) % 10)

        # Problem states the third mode should always be 0 / False
        assert mode_C is False

        if opcode in [1, 2]:
            val_1 = read(data, pointer, 1, mode_A)
            val_2 = read(data, pointer, 2, mode_B)

            if opcode == 1:
                write(data, pointer, 3, val_1 + val_2)
            else:
                write(data, pointer, 3, val_1 * val_2)
            pointer += 4

        elif opcode == 3:
            write(data, pointer, 1, data_input.popleft())
            pointer += 2

        elif opcode == 4:
            # print(data[data[pointer + 1]])
            program_output = data[data[pointer + 1]]
            yield program_output, False
            data_input = yield
            pointer += 2

        elif opcode == 5:
            flag = read(data, pointer, 1, mode_A)
            if flag != 0:
                pointer = read(data, pointer, 2, mode_B)
            else:
                pointer += 3

        elif opcode == 6:
            flag = read(data, pointer, 1, mode_A)
            if flag == 0:
                pointer = read(data, pointer, 2, mode_B)
            else:
                pointer += 3

        elif opcode == 7:
            v1 = read(data, pointer, 1, mode_A)
            v2 = read(data, pointer, 2, mode_B)
            store = 1 if v1 < v2 else 0
            write(data, pointer, 3, store)
            pointer += 4

        elif opcode == 8:
            v1 = read(data, pointer, 1, mode_A)
            v2 = read(data, pointer, 2, mode_B)
            store = 1 if v1 == v2 else 0
            write(data, pointer, 3, store)
            pointer += 4

        elif opcode == 99:
            break

        else:
            raise Exception("Unexpected instruction at {}: {}".format(pointer, opcode))
    yield program_output, True


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
