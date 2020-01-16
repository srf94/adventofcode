from utils import read_data


data = read_data(1)


print("Part 1:")
print(sum((int(row) // 3) - 2 for row in data))


total = 0
for row in data:
    fuel = 0
    remaining = int(row)
    while True:
        remaining = (remaining // 3) - 2
        if remaining <= 0:
            break
        fuel += remaining
    total += fuel


print("Part 2:")
print(total)
