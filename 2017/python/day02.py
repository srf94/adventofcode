import itertools

with open('../input/day02.txt', 'r') as f:
	data = f.read()

# Remove \t and \n from input and remove empty rows
rows = [[int(j) for j in i.split("\t") if j] 
         for i in data.split("\n")]
rows = [i for i in rows if i]

checksum = sum(max(row) - min(row) for row in rows)
print "Part 1: %s" % checksum

checksum = 0
for row in rows:
	for i, j in itertools.combinations(row, 2):
		a = min(i, j)
		b = max(i, j)
		if not b % a:
			# Have found our matching pair
			checksum += b / a
			break

print "Part 2: %s" % checksum

