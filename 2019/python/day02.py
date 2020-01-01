import copy
import itertools
from utils import read_data
from intcode_vm import IntcodeVM


raw = read_data(2)
raw = raw[0].split(",")


def run_opcode(data, noun, verb):
    data = copy.copy(data)
    data[1] = str(noun)
    data[2] = str(verb)

    for i in range(0, len(data), 4):
        op = data[i]
        input_1 = data[i + 1]
        input_2 = data[i + 2]
        out = data[i + 3]

        val_1 = int(data[int(input_1)])
        val_2 = int(data[int(input_2)])

        if op == "1":
            data[int(out)] = val_1 + val_2
        elif op == "2":
            data[int(out)] = val_1 * val_2
        elif op == "99":
            break
        else:
            raise Exception("Unexpected op code: {}".format(op))

    return data[0]


# Original solution
print ("Part 1:")
print (run_opcode(raw, 12, 2))


for noun, verb in itertools.product(range(100), range(100)):
    result = run_opcode(raw, noun, verb)

    if int(result) == 19690720:
        print ("Part 2:")
        print 100 * noun + verb
        break


# Later solved using full intcode VM
vm = IntcodeVM(raw, mutate_input={1: 12, 2: 2})
vm.run()
print ("Part 1 (using full intcode vm):")
print (vm.D[0])


for noun, verb in itertools.product(range(100), range(100)):
    vm = IntcodeVM(raw, mutate_input={1: noun, 2: verb})
    vm.run()
    result = vm.D[0]

    if int(result) == 19690720:
        print ("Part 2 (using full intcode vm):")
        print 100 * noun + verb
        break
