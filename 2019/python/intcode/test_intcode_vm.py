import pytest
from vm import IntcodeVM


@pytest.mark.parametrize(
    "program,expected",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_day_2_examples(program, expected):
    vm = IntcodeVM(program)
    vm.run()
    assert vm.D_list == expected


def test_day_5_examples():
    program = [3, 0, 4, 0, 99]
    vm = IntcodeVM(program, input_=123)
    result = vm.run()
    assert result == 123
    result = vm.run()
    assert result is None

    program = [1002, 4, 3, 4, 33]
    expected = [1002, 4, 3, 4, 99]
    vm = IntcodeVM(program)
    vm.run()
    assert vm.D_list == expected

    program = [104, 1, 4, 2, 104, 3, 99]
    result = IntcodeVM(program, input_=1).collect_all_outputs()
    assert result == [1, 4, 3]

    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    vm = IntcodeVM(program, input_=10)
    result = vm.run()
    assert result == 0
    vm = IntcodeVM(program, input_=8)
    result = vm.run()
    assert result == 1

    program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    vm = IntcodeVM(program, input_=8)
    result = vm.run()
    assert result == 0
    vm = IntcodeVM(program, input_=7)
    result = vm.run()
    assert result == 1

    program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    vm = IntcodeVM(program, input_=0)
    result = vm.run()
    assert result == 0
    vm = IntcodeVM(program, input_=4)
    result = vm.run()
    assert result == 1

    program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    vm = IntcodeVM(program, input_=0)
    result = vm.run()
    assert result == 0
    vm = IntcodeVM(program, input_=4)
    result = vm.run()
    assert result == 1

    # fmt: off
    program = [
        3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
        1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
        999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99,
    ]
    # fmt: on
    vm = IntcodeVM(program, input_=5)
    result = vm.run()
    assert result == 999
    vm = IntcodeVM(program, input_=8)
    result = vm.run()
    assert result == 1000
    vm = IntcodeVM(program, input_=10)
    result = vm.run()
    assert result == 1001


def test_day_9_examples():
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    vm = IntcodeVM(program)
    result = vm.collect_all_outputs()
    assert result == program

    program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    vm = IntcodeVM(program)
    result = vm.run()
    assert result == 1219070632396864

    program = [104, 1125899906842624, 99]
    vm = IntcodeVM(program)
    result = vm.run()
    assert result == 1125899906842624
