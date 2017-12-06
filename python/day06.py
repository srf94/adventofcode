
with open('input/day06.txt', 'r') as f:
	data = f.read()

data = [int(i) for i in data.split()]

def answer(banks, part_2_target=None):
	count = 0
	states = set()
	N = len(banks)

	while True:
		if banks == part_2_target and count:
			break
		elif tuple(banks) in states:
			break

		states.add(tuple(banks))

		loc = banks.index(max(banks))
		distribute = banks[loc]
		banks[loc] = 0

		for _ in range(distribute):
			loc = (loc + 1) % N
			banks[loc] += 1
		count += 1

	return count, banks

part_1_count, part_1_data = answer(data)
print "Part 1: %s" % part_1_count

part_2_count, _ = answer(part_1_data)
print "Part 2: %s" % part_2_count
