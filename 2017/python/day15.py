

with open('../input/day15.txt', 'r') as f:
    data = f.read().splitlines()
    A = int(data[0].split(" with ")[1].rstrip("'"))
    B = int(data[1].split(" with ")[1].rstrip("'"))

scale = 2147483647


def generate(start, factor, modulo=1):
    x = start

    while True:
        x = x * factor % scale
        if x % modulo == 0:
            yield x & 0xFFFF

ga, gb = generate(A, 16807), generate(B, 48271)
part_1 = sum(ga.next() == gb.next() for _ in range(40000000))
print "Part 1: %s" % part_1

ga, gb = generate(A, 16807, modulo=4), generate(B, 48271, modulo=8)
part_2 = sum(ga.next() == gb.next() for _ in range(5000000))
print "Part 2: %s" % part_2
