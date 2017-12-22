import numpy as np

with open('../input/day22.txt', 'r') as f:
    data = f.read().splitlines()

# data = """..#
# #..
# ...""".splitlines()

def create_grid(data):
	grid = {}
	mid = (len(data) - 1) / 2

	for row_loc, row in enumerate(data):
		for col_loc, val in enumerate(row):
			grid[(col_loc - mid, mid - row_loc)] = val

	return grid

d = np.array([0, 1])
position = np.array([0, 0])

infections = 0
grid = create_grid(data)

for burst in range(10000):
	current = grid.get(tuple(position), ".")

	if current == ".":
		d = np.array([-d[1], d[0]])
		new = "#"
		infections += 1

	else:
		d = np.array([d[1], -d[0]])
		new = "."

	grid[tuple(position)] = new
	position += d

print "Part 1: %s" % infections


d = np.array([0, 1])
position = np.array([0, 0])

infections = 0
grid = create_grid(data)

for burst in range(10000000):
	current = grid.get(tuple(position), ".")

	if current == ".":
		d = np.array([-d[1], d[0]])
		new = "W"

	elif current == "W":
		infections += 1
		new = "#"

	elif current == "#":
		d = np.array([d[1], -d[0]])
		new = "F"

	elif current == "F":
		d = -d
		new = "."

	else:
		raise Exception()

	grid[tuple(position)] = new
	position += d

print "Part 2: %s" % infections

