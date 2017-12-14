
with open('../input/day12.txt', 'r') as f:
	data = f.read().strip()

pipes = {}
for line in data.splitlines():
	n, others = line.split(" <-> ")
	n = int(n)
	others = [int(i.strip()) for i in others.split(",")]

	pipes[n] = others


def get_group(loc, group=None):
	for i in pipes[loc]:
		if i not in group:
			group.add(i)
			group = get_group(i, group)
	return group

loc = 0
group_count = 0
end = max(pipes)
seen_so_far = set()

while True:
	group_count += 1
	group = get_group(loc, {loc})

	if loc == 0:
		print "Part 1: %s" % len(group)

	seen_so_far = seen_so_far.union(group)
	while loc in seen_so_far:
		loc += 1

	if loc > end:
		break

print "Part 2: %s" % group_count
