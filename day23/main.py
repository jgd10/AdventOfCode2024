from aoc import parse_file, InputType, timer, TimeUnit
import networkx as nx


def parse(input_type: InputType):
    data = parse_file(input_type)
    network = {}
    starts_with_t = set()
    for row in data:
        computers = row.split('-')
        cpu1, cpu2 = computers
        if cpu1 not in network:
            network[cpu1] = set()
        if cpu2 not in network:
            network[cpu2] = set()
        network[cpu1].add(cpu2)
        network[cpu2].add(cpu1)
        if cpu1.startswith('t'):
            starts_with_t.add(cpu1)
        if cpu2.startswith('t'):
            starts_with_t.add(cpu2)
    return network, starts_with_t


def find_triangle(network, key):
    connections = network[key]
    loops = set()
    for connection in connections:
        connections2 = network[connection]
        for c2 in connections2:
            connections3 = network[c2]
            if key in connections3:
                loops.add((connection, key, c2))
    return loops

@timer(TimeUnit.ms)
def part1(input_type: InputType):
    netwk, tpooters = parse(input_type)
    loops1 = [find_triangle(netwk, k) for k in netwk]
    loops = {tuple(sorted(loop)) for row in loops1 for loop in row}
    loops = {loop for loop in loops if set(loop).intersection(tpooters)}
    print(f'Part 1: {len(loops)}')


@timer(TimeUnit.ms)
def part2(input_type: InputType):
    graph = nx.Graph()
    data = parse_file(input_type)
    graph.add_edges_from([row.split('-') for row in data])
    triangles = nx.triangles(graph)
    max_num = max([v for v in triangles.values()])
    groups = []
    for k, v in triangles.items():
        group = [k]
        if v == max_num:
            group.extend([n for n in graph.neighbors(k) if triangles[n] == max_num])
            groups.append(group)
    groups = {tuple(sorted(g)) for g in groups}
    codes = [','.join(list(g)) for g in groups]
    code = sorted(codes, key=len).pop()
    print(f'Part 2: {code}')


if __name__ == '__main__':
    part1(InputType.INPUT)
    part2(InputType.INPUT)