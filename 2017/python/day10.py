import copy

with open('../input/day10.txt', 'r') as f:
	data = f.read().strip()

def round(lengths, num=1):
	N = 256
	cur = 0
	skip = 0
	array = range(N)

	for _ in range(num):
		for l in lengths:
			length = int(l)

			new = copy.copy(array)
			for i in range(length):
				new[(cur+length-i-1) % N] = array[(cur+i) % N]

			array = new
			cur = (cur + length + skip) % N
			skip = (skip + 1) % N

	return array

def sparse_to_dense(array):
	output = []
	for i in range(16):
		segment = array[16*i: 16*(i+1)]
		xor = reduce(lambda a, b: a ^ b, segment, 0)
		output.append(xor)
	return output

def to_hex(dense):
	hexes = []
	for i in dense:
		h = hex(i)[2:]
		hexes.append('0' + h if len(h) == 1 else h)

	return "".join(hexes)

part_1 = round(data.split(","))
print "Part 1: %s" % (part_1[0] * part_1[1])

suffix = [17, 31, 73, 47, 23]
ascii_ = [ord(i) for i in data]
ascii_ = ascii_ + suffix

sparse = round(ascii_, num=64)
dense = sparse_to_dense(sparse)

print "Part 2: %s" % to_hex(dense)
