
with open('input/day05.txt', 'r') as f:
	data_in = f.read()

data_1 = [int(i) for i in data_in.splitlines()]
data_2 = [int(i) for i in data_in.splitlines()]

def answer(data, part_2=False):
	steps = 0
	position = 0
	upper_bound = len(data) - 1

	while 0 <= position <= upper_bound:
		steps += 1
		new_position = position + data[position]

		if data[position] >= 3 and part_2:
			data[position] -= 1
		else:
			data[position] += 1

		position = new_position

	return steps

print "Part 1: %s" % answer(data_1)
print "Part 2: %s" % answer(data_2, part_2=True)

