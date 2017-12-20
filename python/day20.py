import numpy as np
from collections import defaultdict

with open('../input/day20.txt', 'r') as f:
    data = f.read().splitlines()


class Particle(object):
    def __init__(self, P, V, A, num=None):
        self.P = P
        self.V = V
        self.A = A

        self.num = num
        self.collided = False

    @classmethod
    def from_string(cls, string, num=None):
        p, v, a = string.split(", ")
        P = np.array([int(i) for i in p[3:-1].split(",")])
        V = np.array([int(i) for i in v[3:-1].split(",")])
        A = np.array([int(i) for i in a[3:-1].split(",")])

        return Particle(P, V, A, num=num)

    def field_size(self, field):
        fields = {
            "P": self.P,
            "V": self.V,
            "A": self.A,
        }

        assert field in fields.keys()
        return np.abs(fields[field]).sum()

    def move(self):
        self.V += self.A
        self.P += self.V


a_min = None
particles = []
for num, i in enumerate(data):
    particle = Particle.from_string(i, num=num)
    particles.append(particle)

    a_size = particle.field_size("A")
    if a_min is None or a_min > a_size:
        a_min = a_size
        closest_n = [num]

    elif a_min == a_size:
        closest_n.append(num)


# If we have multiple particles with the same acceleration it suffices 
# to look at a point in time >> the magnitude of the acceleration
if len(closest_n) > 1:
    scale = 100 * a_size
    distances = {}
    for n in closest_n:
        particle = Particle.from_string(data[n])
        for _ in xrange(scale):
            particle.move()
        distances[n] = particle.field_size("P")

    min_dist = min(distances.values())
    closest_n = [n for n, dist in distances.items() if dist == min_dist]

print "Part 1: %s" % closest_n[0]


for kk in range(100):
    for particle in particles:
        particle.move()

    positions = defaultdict(list)
    for particle in particles:
        positions[tuple(particle.P)].append(particle)

    for p_list in positions.values():
        if len(p_list) > 1:
            for particle in p_list:
                particle.collided = True

    particles = [p for p in particles if not p.collided]

print "Part 2: %s" % len(particles)
