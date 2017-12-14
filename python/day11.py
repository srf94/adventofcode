import numpy as np

with open('../input/day11.txt', 'r') as f:
	data = f.read().strip().split(",")

def distance(loc):
	# First come back diagonally
	d = abs(loc[1])

	if abs(loc[0]) > abs(loc[1]):
		new_x = (-1 if loc[0] < 0 else 1) * (abs(loc[0]) - abs(loc[1]))
		loc = np.array([new_x, 0])
		d += abs(loc[0]) / 2

	return d


directions = {
	"n": np.array([2, 0]),
	"ne": np.array([1, 1]),
	"nw": np.array([1, -1]),
	"s": np.array([-2, 0]),
	"se": np.array([-1, 1]),
	"sw": np.array([-1, -1]),
}

new_distance = 0
location = np.array([0, 0])
for i in data:
	location += directions[i]
	new_distance = max(new_distance, distance(location))

final_distance = distance(location)

print "Part 1: %s" % final_distance
print "Part 2: %s" % new_distance
