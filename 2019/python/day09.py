from utils import read_data
from intcode_vm import run_instructions, intcode_send


raw = read_data(9)[0].split(",")


gen = run_instructions(raw, debug=False)
value = 1
while True:
    try:
        value = intcode_send(gen, value)
    except StopIteration:
        break


print("Part 1:")
print(value)


gen = run_instructions(raw, debug=False)
value = 2
while True:
    try:
        value = intcode_send(gen, value)
    except StopIteration:
        break


print("Part 2:")
print(value)
