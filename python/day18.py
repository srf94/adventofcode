from collections import defaultdict

with open('../input/day18.txt', 'r') as f:
    data = f.read().splitlines()


class Program(object):
    def __init__(self, data, p, part_1=True):
        self.data = data
        self.part_1 = part_1

        self.loc = 0
        self.queue = []
        self.counter = 0
        self.waiting = False
        self.last_played = None

        self.R = defaultdict(int)
        self.R['p'] = p

    def val(self, val):
        try:
            return int(val)
        except:
            return self.R[val]

    def step(self):
        if self.loc >= len(self.data):
            self.waiting = True
            return

        s = data[self.loc].split()
        name = s[0]
        X = s[1]
        if len(s) > 2:
            Y = s[2]

        if name == "snd":
            if self.part_1:
                self.last_played = self.R.get(X)
            else:
                self.loc += 1
                self.counter += 1
                return "snd", self.val(X)

        elif name == "set":
            self.R[X] = self.val(Y) 

        elif name == "add":
            self.R[X] += self.val(Y) 

        elif name == "mul":
            self.R[X] *= self.val(Y) 

        elif name == "mod":
            self.R[X] %= self.val(Y) 

        elif name == "rcv":
            if self.part_1:
                print "Part 1: %s" % self.last_played
                return True

            if self.queue:
                self.R[X] = self.queue.pop(0)
            else:
                self.waiting = True
                return

        elif name == "jgz":
            if self.val(X) > 0:
                self.loc += self.val(Y) - 1

        self.loc += 1


# Part 1
program = Program(data, 0, part_1=True)
complete = False
while not complete:
    complete = program.step()

# Part 2
run = "a"
program_a = Program(data, 0, part_1=False)
program_b = Program(data, 1, part_1=False)

running, dormant = program_a, program_b

while True:
    if program_a.waiting and program_b.waiting:
        break

    res = program_a.step()
    if res and res[0] == "snd":
        program_b.queue.append(res[1])

    res = program_b.step()
    if res and res[0] == "snd":
        program_a.queue.append(res[1])

print "Part 2: %s" % program_b.counter
