
class Tower(object):
    def __init__(self):
        with open('../input/day07.txt', 'r') as f:
            data = f.read()
            data = data.splitlines()

        self.base = None
        self.children = {}
        self.parents = {}
        self.weights = {}
        self.total_weights = {}

        for line in data:
            elements = [i.strip().strip(",") for i in line.split(" ")]
            name = elements[0]
            weight = int(elements[1][1:-1])
            self.weights[name] = weight

            if len(elements) > 2:
                self.children[name] = elements[3:]

                for child in elements[3:]:
                    self.parents[child] = name

    def part_1(self):
        self.get_base()
        print "Part 1: %s" % self.base

    def part_2(self):
        # First calculate the total weights for every disk, starting from the bottom
        self.calc_disk_weight(self.base)

        # Now pass through the tower a second time from the bottom
        # At each stage, follow the path with an uneven weight
        print "Part 2: %s" % self.get_new_weight(self.base, None)

    def get_base(self):
        # Walk the tree to the parent
        name = self.parents.keys()[0]

        while True:
            if self.parents.get(name):
                name = self.parents.get(name)
            else:
                break
        self.base = name

    def calc_disk_weight(self, name):
        c_weights = [self.calc_disk_weight(i) for i in self.children.get(name, [])]

        self.total_weights[name] = self.weights[name] + sum(c_weights)
        return self.total_weights[name]

    def get_new_weight(self, name, target_weight):
        children = self.children.get(name, [])
        c_weights = [self.total_weights[c] for c in children]
        matching = [c_weights[0] == i for i in c_weights[1:]]

        if all(matching):
            return str(int(target_weight) - sum(c_weights))

        elif all(not i for i in matching):
            name = children[0]
            target_weight = c_weights[1]
            return self.get_new_weight(name, target_weight)
        else:
            name = children[matching.index(False)+1]
            target_weight = c_weights[0]
            return self.get_new_weight(name, target_weight)


tower = Tower()
tower.part_1()
tower.part_2()

