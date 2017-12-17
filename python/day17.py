
step = 376

pos = 0
buf = [0]
for i in range(1, 2018):
	pos = (pos + step) % len(buf) + 1
	buf = buf[:pos] + [i] + buf[pos:]

print "Part 1: %s" % buf[buf.index(2017) + 1]


pos = 0
buf = {0: 0}
for i in range(1, 2018):
	for _ in range(step+1):
		pos = buf[pos]
 	pointer = buf[pos]
	buf[pos] = i
	buf[i] = pointer

print "Alternate Part 1 (Linked List): %s" % buf[2017]

pos = 0
ans = None
for i in range(1, 50000000):
	pos = (pos + step) % i + 1
	if pos == 1:
		ans = i

print "Part 2: %s" % ans
