from utils import read_data
from intcode.vm import IntcodeVM


raw = read_data(21)[0].split(",")


def attempt(instructions):
    instructions.append("WALK")
    text_input = [ord(i) for i in "\n".join(instructions) + "\n"]

    vm = IntcodeVM(raw, input_=text_input)
    out = vm.collect_all_outputs()

    buffer = []
    for i in out:
        if i == 10:
            print("".join(buffer))
            buffer = []
        else:
            try:
                buffer.append(chr(i))
            except ValueError:
                # final instruction is puzzle result
                print("Part 1:")
                print(i)


part_1_instructions = [
    "NOT A T",
    "NOT B J",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
]
attempt(part_1_instructions)
