from utils import read_data


raw = read_data(6)
data = [i.split(")") for i in raw]
orbit_graph = {orbiter: orbited for orbited, orbiter in data}


def get_child_orbits(graph_dict, node):
    print("Getting orbit for node {}".format(node))
    try:
        return 1 + graph_dict[node]
    except KeyError:
        try:
            child = orbit_graph[node]
        except KeyError:
            graph_dict[node] = 0
            return 0
        graph_dict[node] = get_child_orbits(graph_dict, child)
        return 1 + graph_dict[node]


orbit_graph_dict = {}
total = 0
for k in orbit_graph:
    total += get_child_orbits(orbit_graph_dict, k)

print("Part 1:")
print(total)


def get_chain(planet):
    chain = []
    while True:
        chain.append(planet)
        planet = orbit_graph.get(planet)
        if planet is None:
            return chain


santa_chain = get_chain("SAN")
my_chain = get_chain("YOU")
my_chain_set = set(my_chain)


for count_1, planet in enumerate(santa_chain[1:]):
    if planet in my_chain_set:
        common_planet = planet
        break

for count_2, planet in enumerate(my_chain[1:]):
    if planet == common_planet:
        break

print("Part 2:")
print(count_1 + count_2)
