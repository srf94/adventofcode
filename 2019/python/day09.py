from utils import read_data
from intcode_vm import IntcodeVM


raw = read_data(9)[0].split(",")


print("Part 1:")
print(IntcodeVM(raw, input_=1).run())


print("Part 2:")
print(IntcodeVM(raw, input_=2).run())
