from math import ceil
from utils import read_data


def make_dependency_graph(raw):
    dependency = {}
    for line in raw:
        ing, makes = line.split('=')
        q, name = makes.strip('>').strip().split(' ')

        i = {}
        for k in ing.split(','):
            qq, ii = k.strip().split(' ')
            i[ii] = int(qq)

        assert name not in dependency
        dependency[name] = {'q': int(q.strip()), 'i': i}
    return dependency


def parse_graph(dependency_graph, part):
    needed = {'FUEL': 1}
    keys_remaining = set(dependency_graph.keys())

    while True:
        for key in keys_remaining:
            bad = False
            for k in keys_remaining:
                if key in dependency_graph[k]['i'].keys():
                    bad = True
                    break
            if not bad:
                keys_remaining.remove(key)
                break
        else:
            break

        dep = dependency_graph.get(key)
        need = needed[key]

        if dep is None:
            continue

        quantity = need / float(dep['q'])
        if part == 1:
            quantity = int(ceil(quantity))

        for k, v in dep['i'].items():
            needed[k] = needed.get(k, 0) + quantity * v

    return needed


def total_ore_needed(dependency_graph, needed):
    ore_touching = {k for k, v in dependency_graph.items() if 'ORE' in v['i']}

    ore = 0
    for key in ore_touching:
        need = needed[key]
        dep = dependency_graph[key]
        quantity = need / float(dep['q'])
        ore += quantity * dep['i']['ORE']
    return ore


raw = read_data(14)
dependency_graph = make_dependency_graph(raw)


needed = parse_graph(dependency_graph, 1)
print("Part 1:")
print(int(total_ore_needed(dependency_graph, needed)))


needed = parse_graph(dependency_graph, 2)
print("Part 2:")
ore_needed = total_ore_needed(dependency_graph, needed)
print(int(float(1000000000000) / ore_needed))
