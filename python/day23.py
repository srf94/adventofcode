import numpy as np
from collections import defaultdict

with open('../input/day23.txt', 'r') as f:
    data = f.read().splitlines()

class Program(object):
    def __init__(self, data, part_1=True):
        self.data = data
        self.part_1 = part_1

        self.loc = 0
        self.mul_count = 0

        self.R = defaultdict(int)
        if not self.part_1:
            self.R['a'] = 1

    def val(self, val):
        try:
            return int(val)
        except:
            return self.R[val]

    def step(self):
        if self.loc < 0 or len(self.data) <= self.loc:
            return True

        name, X, Y = data[self.loc].split()

        if name == "set":
            self.R[X] = self.val(Y) 

        elif name == "sub":
            self.R[X] -= self.val(Y) 

        elif name == "mul":
            self.R[X] *= self.val(Y) 
            self.mul_count += 1

        elif name == "jnz":
            if self.val(X) != 0:
                self.loc += self.val(Y) - 1

        self.loc += 1


def prime(n):
    if n < 2:
        return False
    for x in xrange(2, int(n**0.5) + 1):
        if n % x == 0:
            return False
    return True


program = Program(data)
finished = False
while not finished:
    finished = program.step()

print "Part 1: %s" % program.mul_count


b = 84*100 + 100000
c = b + 17000
h = 0

for i in range(b, c + 1, 17):
    if not prime(i):
        h += 1

print "Part 2: %s" % h
