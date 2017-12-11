
with open('../input/day01.txt', 'r') as f:
	data = f.read().strip("\r\n")

data = [int(i) for i in data]
N = len(data)

part_1 = sum(i for loc, i in enumerate(data) if data[loc] == data[(loc+1)%N])
print "Part 1: %s" % part_1

part_2 = sum(i for loc, i in enumerate(data) if data[loc] == data[(loc+N/2)%N])
print "Part 2: %s" % part_2
