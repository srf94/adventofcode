
with open('../input/day04.txt', 'r') as f:
	data = f.read()

data = data.splitlines()

def answer(data, anagram):
	valid_phrases = 0
	for line in data:
		if anagram:
			words = ["".join(sorted(i)) for i in line.split(" ")]
		else:
			words = line.split(" ")

		count = set(words)
		if len(words) == len(count):
			valid_phrases += 1

	return valid_phrases

print "Part 1: %s" % answer(data, False)
print "Part 2: %s" % answer(data, True)

