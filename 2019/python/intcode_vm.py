def extended_read(data, value):
    assert value >= 0
    try:
        return data[value]
    except IndexError:
        return 0


def read(data, pointer, increment, mode, relative_base, debug):
    loc = pointer + increment
    assert loc >= 0
    parameter = extended_read(data, loc)
    if debug:
        print("Read input parameter: {}".format(parameter))

    assert mode in [0, 1, 2]

    if mode == 0:
        assert parameter >= 0
        value = extended_read(data, parameter)
        if debug:
            print("(mode=0) Reading from pointer {}, value: {}".format(parameter, value))
        return value

    if mode == 1:
        if debug:
            print("(mode=1) Using read parameter {}".format(parameter))
        return parameter

    parameter = parameter + relative_base
    assert parameter >= 0
    value = extended_read(data, parameter)
    if debug:
        print("(mode=0) Reading from pointer {}, value: {}".format(parameter, value))
    return value



def write(data, pointer, increment, new_value, debug, mode, relative_base):
    loc = pointer + increment
    assert loc >= 0
    write_loc = extended_read(data, loc)

    if mode == 2:
        if debug:
            print("Writing in mode 2, changing pointer from {} to {}".format(write_loc, write_loc + relative_base))
        write_loc = write_loc + relative_base

    if mode == 1:
        print("Mode 1 when writing!")
        import pdb
        pdb.set_trace()

    old_value = extended_read(data, write_loc)
    if debug:
        print("Writing to pointer {}: {} -> {}".format(write_loc, old_value, new_value))
    try:
        data[write_loc] = new_value
    except IndexError:
        if write_loc > 100000:
            import pdb
            pdb.set_trace()
        data.extend([0 for _ in range(len(data), write_loc+1)])
        data[write_loc] = new_value



def run_instructions(data, debug=False):
    data_input = yield
    pointer = 0
    relative_base = 0
    program_output = "No output given!"

    while True:
        assert pointer >= 0
        instruction = extended_read(data, pointer)
        opcode = instruction % 100

        mode_A = (instruction // 100) % 10
        mode_B = (instruction // 1000) % 10
        mode_C = (instruction // 10000) % 10

        if debug:
            print()
            print('New opcode: {}, pointer {}'.format(instruction, pointer))
            print(data[pointer: pointer+6])

        if opcode in [1, 2]:
            val_1 = read(data, pointer, 1, mode_A, relative_base, debug)
            val_2 = read(data, pointer, 2, mode_B, relative_base, debug)

            if opcode == 1:
                write(data, pointer, 3, val_1 + val_2, debug, mode_C, relative_base)
            else:
                write(data, pointer, 3, val_1 * val_2, debug, mode_C, relative_base)
            pointer += 4

        elif opcode == 3:
            to_write = data_input.popleft()
            if debug:
                print("About to write input {}".format(to_write))
            write(data, pointer, 1, to_write, debug, mode_A, relative_base)
            pointer += 2

        elif opcode == 4:
            assert pointer >= -1
            program_output_old = program_output
            program_output = read(data, pointer, 1, mode_A, relative_base, debug)
            if debug:
                print("program_output: {} -> {}".format(program_output_old, program_output))
            yield program_output, False
            data_input = yield
            pointer += 2

        elif opcode == 5:
            flag = read(data, pointer, 1, mode_A, relative_base, debug)
            if flag != 0:
                if debug:
                    print("Flag {} != 0".format(flag))
                old_pointer = pointer
                pointer = read(data, pointer, 2, mode_B, relative_base, debug)
                if debug:
                    print("Pointer {} -> {}".format(old_pointer, pointer))
            else:
                if debug:
                    print("Flag {} == 0".format(flag))
                    print("Pointer {} -> {}".format(pointer, pointer + 3))
                pointer += 3

        elif opcode == 6:
            flag = read(data, pointer, 1, mode_A, relative_base, debug)
            if flag == 0:
                if debug:
                    print("Flag {} == 0".format(flag))
                pointer = read(data, pointer, 2, mode_B, relative_base, debug)
            else:
                if debug:
                    print("Flag {} != 0".format(flag))
                pointer += 3

        elif opcode == 7:
            v1 = read(data, pointer, 1, mode_A, relative_base, debug)
            v2 = read(data, pointer, 2, mode_B, relative_base, debug)
            store = 1 if v1 < v2 else 0
            msg = "was" if v1 < v2 else "not"
            if debug:
                print("Value 1 {} {} less than value 2 {}".format(v1, msg, v2))
            write(data, pointer, 3, store, debug, mode_C, relative_base)
            pointer += 4

        elif opcode == 8:
            v1 = read(data, pointer, 1, mode_A, relative_base, debug)
            v2 = read(data, pointer, 2, mode_B, relative_base, debug)
            store = 1 if v1 == v2 else 0
            msg = "equals" if v1 == v2 else "does not equal"
            if debug:
                print("Value 1 {} {} value 2 {}".format(v1, msg, v2))
            write(data, pointer, 3, store, debug, mode_C, relative_base)
            pointer += 4

        elif opcode == 9:
            value = read(data, pointer, 1, mode_A, relative_base, debug)
            if debug:
                print("Relative base changed: {} -> {}".format(relative_base, relative_base+value))
            relative_base += value
            pointer += 2

        elif opcode == 99:
            if debug:
                print("Opcode 99 - terminating with output {}".format(program_output))
            break

        else:
            raise Exception("Unexpected instruction at {}: {}".format(pointer, opcode))

    yield program_output, True