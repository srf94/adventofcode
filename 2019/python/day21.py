from utils import read_data
from intcode.vm import IntcodeVM


raw = read_data(21)[0].split(",")


def attempt(instructions, part):
    assert part in [1, 2]
    if part == 1:
        instructions.append("WALK")
    else:
        instructions.append("RUN")

    text_input = [ord(i) for i in "\n".join(instructions) + "\n"]
    vm = IntcodeVM(raw, input_=text_input)
    out = vm.collect_all_outputs()

    row = []
    for i in out:
        if i == 10:
            # print("".join(row))
            row = []
        else:
            try:
                row.append(chr(i))
            except ValueError:
                # final instruction is puzzle result
                print("Part {}:".format(part))
                print(i)


"""
Part 1 jumps
Jump 1:
#####.###########

Jump 2:
#####..#.########
Must jump when A=1, B=0, C=0, D=1
Must jump when A=0, B=1, C=1, D=1

Jump 3:
#####...#########
Must jump when A=0, B=0, C=0

Jump 4:
#####.##.########
Can jump when A=1, B=0, C=1, D=1
or A=1, B=1, C=0, D=1

Jump 5:
#####.#.#########
Must jump when A=1, B=1, C=0, D=1
Must jump when A=0, B=1, C=1, D=1

Jump 6:
#####.#..########
Must jump when A=1, B=1, C=0, D=1
Must jump when A=0, B=0, C=1, D=1

Suitable instructions:
D=1 AND (A=0 OR B=0 OR C=0)
"""


part_1_instructions = ["NOT A T", "NOT B J", "OR T J", "NOT C T", "OR T J", "AND D J"]
attempt(part_1_instructions, 1)


"""
Part 2 jumps
Jump 7:
#####.#.#..##.###
Must jump when A=0, B=1, C=0, D=1, E=0, F=0, G=1, H=1, I=0
Must jump when A=0, B=0, C=1, D=1, E=0, F=1, G=1, H=1, I=1
Must jump when A=0, B=1, C=1, D=1, E=1, F=1, G=1, H=1, I=1

Jump 8:
#####..#.#.#..###
Must jump when A=1, B=0, C=0, D=1, E=0, F=1, G=0, H=1, I=0
Must jump when A=0, B=1, C=0, D=1, E=0, F=0, G=1, H=1, I=1
Must jump when A=0, B=0, C=1, D=1, E=1, F=1, G=1, H=1, I=1

Jump 9:
#####..####..####
Must jump when A=0, B=0, C=1, D=1, E=1, F=1, G=0, H=0, I=1
OR             A=1, B=0, C=0, D=1, E=1, F=1, G=1, H=0, I=0

Jump 10:
#####...##.#.####
Must jump when A=0, B=0, C=0, D=1, E=1, F=0, G=1, H=0, I=1
Must jump when A=0, B=1, C=0, D=1, E=1, F=1, G=1, H=1, I=1

Suitable instructions:
D=1 AND (A=0 OR B=0 OR C=0) AND (E=1 OR H=1)
"""


part_2_instructions = [
    "NOT A T",
    "NOT B J",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT E T",
    "NOT T T",
    "OR H T",
    "AND T J",
]
attempt(part_2_instructions, 2)
