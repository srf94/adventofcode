
with open('../input/day09.txt', 'r') as f:
	data = f.read().strip()

score = 0
garbage_count = 0

nest = 0
garbage = False
cancel = False
for char in data:
	if cancel:
		cancel = False
		continue

	if char == "{" and not garbage:
		nest += 1
	elif char == "}" and not garbage:
		score += nest
		nest -= 1
	elif char == "<" and not garbage:
		garbage = True
	elif char == ">":
		garbage = False
	elif char == "!" and garbage:
		cancel = True
	elif garbage:
		garbage_count += 1

print "Part 1: %s" % score
print "Part 2: %s" % garbage_count
