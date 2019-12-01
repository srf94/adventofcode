
with open('../input/day13.txt', 'r') as f:
	data = f.read().strip().splitlines()

scanners = {}
for layer in data:
	i, j = layer.split(": ")
	scanners[int(i)] = int(j)

def scanner_position(s, depth, time):
	if depth not in s:
		return None

	range_ = s[depth]
	t = time % (2 * (range_ - 1))

	if t < range_:
		return t
	else:
		return 2 * (range_ - 1) - t

def get_severity():
	return sum(t * scanners[t] for t in range(max(scanners) + 1) 
		if scanner_position(scanners, t, t) == 0)


print "Part 1: %s" % get_severity()

wait = 0
while True:
	for time in range(max(scanners) + 1):
		if scanner_position(scanners, time, time + wait) == 0:
			break
	else:
		break
	wait += 1

print "Part 2: %s" % wait
