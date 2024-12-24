from aoc import TimeUnit, parse_file, InputType, timer
from enum import Enum
from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network as PVNetwork


class Operator(Enum):
    AND = 1
    OR = 2
    XOR = 3


@dataclass(frozen=True)
class Command:
    variables: tuple[str, str]
    operator: Operator
    result: str

    @classmethod
    def from_string(cls, string):
        command, result = string
        values = command.split(' ')
        variables = (values[0], values[-1])
        match values[1]:
            case 'AND':
                op = Operator.AND
            case 'OR':
                op = Operator.OR
            case 'XOR':
                op = Operator.XOR
            case _:
                raise ValueError
        return cls(variables, op, result)

    def perform(self, output_values, commands):
        var1, var2 = self.variables
        if output_values[var1] is None:
            command = [c for c in commands if c.result == var1].pop()
            command.perform(output_values, commands)
        if output_values[var2] is None:
            command = [c for c in commands if c.result == var2].pop()
            command.perform(output_values, commands)
        match self.operator:
            case Operator.AND:
                v = output_values[var1] & output_values[var2]
            case Operator.OR:
                v = output_values[var1] | output_values[var2]
            case Operator.XOR:
                v = output_values[var1] ^ output_values[var2]
        output_values[self.result] = v


def parse(input_type: InputType):
    data = parse_file(input_type)
    starting_vals = [row.split(':') for row in data if ':' in row]
    values = {v[0].strip(): int(v[1]) for v in starting_vals}
    operations = [row.split(' -> ')  for row in data if '->' in row]
    operations = [Command.from_string(op) for op in
                  operations]
    for op in operations:
        values[op.result] = None
    return operations, values


def perform_command(command: Command, instructions, values, variable):
    var1, var2 = command.variables
    if values[var1] is None:
        perform_command(instructions[var1], instructions, values, var1)
    if values[var2] is None:
        perform_command(instructions[var2], instructions, values, var2)
    match command.operator:
        case Operator.AND:
            v = values[var1] & values[var2]
        case Operator.OR:
            v = values[var1] | values[var2]
        case Operator.XOR:
            v = values[var1] ^ values[var2]
    values[variable] = v


def values_to_int(n_vals):
    names = []
    vals = []
    for n, v in n_vals.items():
        names.append(n)
        vals.append(v)
    result = int(''.join([str(v) for _, v in sorted(zip(names, vals),
                                                    reverse=True)]), 2)
    return result


def visualise(network):
    net = PVNetwork()
    for k, v in network.nodes.items():
        net.add_node(k)
    for k, v in network.nodes.items():
        for e in v.edges:
            net.add_edge(k, e)
    net.toggle_physics(True)
    net.show('mygraph.html', notebook=False)


@timer(TimeUnit.ms)
def part1(input_type: InputType):
    ops, vals = parse(input_type)
    for op in ops:
        op.perform(vals, ops)
    z_vals = {var: v for var, v in vals.items() if 'z' in var}
    print(f'Part 1: {values_to_int(z_vals)}')


@timer(TimeUnit.s)
def part2(input_type: InputType):
    ops, vals = parse(input_type)
    x_num = values_to_int({var: v for var, v in vals.items() if 'x' in var})
    y_num = values_to_int({var: v for var, v in vals.items() if 'y' in var})
    edges = []
    graph = nx.Graph()
    nodes = set()
    result_nodes = {op.result: op.operator for op in ops}
    for op in ops:
        for n in [*op.variables, op.result]:
            if n not in nodes:
                color = 'gray'
                if n in result_nodes:
                    match result_nodes[n]:
                        case Operator.AND:
                            color = 'crimson'
                        case Operator.OR:
                            color = 'navy'
                        case Operator.XOR:
                            color = 'purple'
                else:
                    color = 'gray'

                graph.add_node(n, color=color)
                nodes.add(n)
        res = op.result
        graph.add_edge(op.variables[0], res)
        graph.add_edge(op.variables[1], res)
    nt = PVNetwork('1000px', '2000px',
                   select_menu = True,
                   filter_menu = True)
    nt.show_buttons(filter_=["physics"])
    nt.from_nx(graph)
    nt.show('nx.html', notebook=False)
    # I solved this visually in the end using pyvis and networkx
    # it was a huge pain and would probably have been quicker to just learn
    # the theory, but alas, and now it is done! I'll hopefully come back and
    # code it up another time

if __name__ == '__main__':
    part1(InputType.INPUT)
    part2(InputType.INPUT)
