from utils import read_data
from itertools import combinations
from collections import deque, namedtuple


def add_direction(loc, d):
    x, y = loc
    if d == 0:
        y += 1
    elif d == 1:
        x += 1
    elif d == 2:
        y -= 1
    elif d == 3:
        x -= 1
    else:
        raise Exception(d)
    return x, y


def get_start_locations(grid):
    return [(x, y) for (x, y), value in grid.items() if value == "@"]


def part_1(raw):
    grid = {(x, y): value for (y, row) in enumerate(raw) for (x, value) in enumerate(list(row))}
    start = get_start_locations(grid)[0]
    all_nodes = {i for i in grid.values() if i.islower()}

    step = namedtuple("step", ("loc", "seen", "d"))
    Q = deque()
    Q.append(step(start, {}, 0))
    SEEN = set()

    while True:
        loc, seen, dist = Q.popleft()

        value = grid.get(loc, "#")
        if value == "#":
            continue

        if value.isupper() and value.lower() not in seen:
            continue

        key = (loc, tuple(sorted(seen)))
        if key in SEEN:
            continue
        SEEN.add(key)

        if value.islower():
            seen = {i for i in seen}
            seen.add(value)
            if seen == all_nodes:
                print("Part 1:")
                print(dist)
                return True

        for d in range(4):
            new_loc = add_direction(loc, d)
            Q.append(step(new_loc, seen, dist + 1))


def create_dependency_graph(grid_dict, start):
    """
    Simplify graph to only include named points (keys, doors, starting point)
    """
    step = namedtuple("step", ("loc", "symbol", "rotate_from"))
    path = [step(start, grid_dict[start], 0)]

    graph = {}
    path_from_origin = {}
    loc = start
    seen = {loc: len(path)}

    while True:
        for d in range(path[-1].rotate_from, 4):
            new_loc = add_direction(loc, d)
            symbol = grid_dict.get(new_loc, "#")
            seen_status = seen.get(new_loc)

            if symbol != "#" and (seen_status is None or len(path) < seen_status):
                path[-1] = step(path[-1].loc, path[-1].symbol, d + 1)
                break
        else:
            if len(path) == 1:
                break

            path.pop()
            loc = path[-1].loc
            continue

        loc = new_loc
        path.append(step(loc, symbol, 0))
        seen[loc] = len(path)

        if symbol.isalpha() and symbol.islower():
            graph[symbol] = [i.symbol for i in path if i.symbol.isalpha() and i.symbol.isupper()]
            path_from_origin[symbol] = [i for i in path[1:]]

    return graph, path_from_origin


def intermediate_symbols(path, key):
    return set(p.symbol for p in path if p.symbol not in ['.', key])


def calculate_distances_and_intermediates(paths_from_origin):
    """
    Calculate distance between points and record keys, doors that lie between them
    """
    keys = sorted(paths_from_origin.keys())

    distances = {("@", k): len(p) for k, p in paths_from_origin.items()}
    intermediates = {("@", k): intermediate_symbols(path, k) for k, path in paths_from_origin.items()}

    for k1, k2 in combinations(keys, 2):
        p1 = paths_from_origin[k1]
        p2 = paths_from_origin[k2]

        p1_locs = [p.loc for p in p1]
        p2_locs = [p.loc for p in p2]
        overlaps = set(p1_locs).intersection(set(p2_locs))

        if not overlaps:
            distance = len(p1) + len(p2)
            intermediate = intermediates["@", k1].union(intermediates["@", k2])

        else:
            p1_len = len(p1)
            p2_len = len(p2)

            distance = None
            for overlap in overlaps:
                d = p1_len - p1_locs.index(overlap) + p2_len - p2_locs.index(overlap) - 2
                if distance is None or d < distance:
                    distance = d
                    used_overlap = overlap

            intermediate = intermediate_symbols(p1[p1_locs.index(used_overlap):], k1).union(
                intermediate_symbols(p2[p2_locs.index(used_overlap):], k2)
            )

        distances[k1, k2] = distance
        intermediates[k1, k2] = intermediate

    # Key ordering does not matter
    distances_copy = list(distances.items())
    for (k1, k2), v in distances_copy:
        distances[k2, k1] = v

    intermediates_copy = list(intermediates.items())
    for (k1, k2), v in intermediates_copy:
        intermediates[k2, k1] = v

    return distances, intermediates


def edit_grid(grid, start):
    delta = [
        (0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]
    for dx, dy in delta:
        loc = (start[0] + dx, start[1] + dy)
        if abs(dx) + abs(dy) == 2:
            grid[loc] = "@"
        else:
            grid[loc] = "#"
    return grid


def part_2(raw):
    grid = {(x, y): value for (y, row) in enumerate(raw) for (x, value) in enumerate(list(row))}
    all_nodes = {i for i in grid.values() if i.islower()}

    start = get_start_locations(grid)[0]
    grid = edit_grid(grid, start)
    robot_starts = get_start_locations(grid)

    graphs, path_from_origin = zip(*[create_dependency_graph(grid, r) for r in robot_starts])
    distances, intermediates = zip(*[calculate_distances_and_intermediates(p) for p in path_from_origin])

    step = namedtuple("step", ("nodes", "seen", "d"))
    Q = deque()
    Q.append(step(["@", "@", "@", "@"], {}, 0))

    SEEN = {}
    while True:
        try:
            nodes, seen, d = Q.popleft()
        except:
            break

        nodes_to_visit = []
        for graph, intermediate, node in zip(graphs, intermediates, nodes):
            seen_upper = {i.upper() for i in seen}
            new_graph_no_doors = {
                k: [i for i in v if i not in seen_upper]
                for k, v in graph.items()
            }
            new_nodes = [
                k for k, v in new_graph_no_doors.items()
                if k not in seen and
                all(i.lower() in seen for i in v) and
                not any(i.islower() and i not in seen for i in intermediate[node, k])
            ]
            nodes_to_visit.append(new_nodes)

        for loc, new_robot_nodes in enumerate(nodes_to_visit):
            for new_node in new_robot_nodes:
                new_nodes = [i for i in nodes]
                new_nodes[loc] = new_node

                seen_nodes = {i for i in seen}
                seen_nodes.add(new_node)

                new_d = d + distances[loc][nodes[loc], new_node]

                if seen_nodes == all_nodes:
                    print("Part 2:")
                    print(new_d)
                    return True

                key = (tuple(new_nodes), tuple(sorted(seen_nodes)))
                existing = SEEN.get(key)

                if existing is None:
                    SEEN[key] = new_d
                    Q.append(step(new_nodes, seen_nodes, new_d))

                elif new_d < existing:
                    SEEN[key] = new_d
                    matching_q = [l for l, q in enumerate(Q) if q[0] == new_nodes and q[1] == seen_nodes]
                    assert len(matching_q) == 1

                    s = Q[matching_q[0]]
                    Q[matching_q[0]] = step(s[0], s[1], new_d)


raw = read_data(18)
part_1(raw)
part_2(raw)
