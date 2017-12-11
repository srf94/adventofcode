from collections import defaultdict
import itertools

with open('../input/day08.txt', 'r') as f:
	data = f.read()
	data = data.splitlines()

reg = defaultdict(int)

max_t = 0
for line in data:
    r, d, s, iff, var, c, i = line.split()

    condition = "reg['%s'] %s %s" % (var, c, i)
    if eval(condition):
        reg[r] += (1 if d == "inc" else -1) * int(s)

    max_t = max(max_t, max(reg.values()))

print "Part 1: %s" % max(reg.values())
print "Part 2: %s" % max_t
