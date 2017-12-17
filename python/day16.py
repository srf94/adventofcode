import string

with open('../input/day16.txt', 'r') as f:
    data = f.read().splitlines()[0].split(",")
N = 16

def dance(P=None):
	if P is None:
		P = list(string.ascii_lowercase[:N])

	for i in data:
		if not i:
			continue

		if i[0] == "s":
			spin = int(i[1:])
			P = P[-spin:] + P[:N-spin]

		elif i[0] == "x":
			try:
				a, b = i[1:].split("/")
			except:
				import pdb
				pdb.set_trace()
			a, b = int(a), int(b)
			P[a], P[b] = P[b], P[a]

		elif i[0] == "p":
			a, b = i[1:].split("/")
			a_i, b_i = P.index(a), P.index(b)
			P[a_i], P[b_i] = b, a

	return P

print "Part 1: %s" % "".join(dance())

P = list(string.ascii_lowercase[:N])
initial = list(string.ascii_lowercase[:N])
i = 0
while True:
	i += 1
	P = dance(P=P)
	if P == initial:
		break

n_dances = 1000000000 % i
P = list(string.ascii_lowercase[:N])
for _ in range(n_dances):
	P = dance(P=P)

print "Part 2: %s" % "".join(P)
