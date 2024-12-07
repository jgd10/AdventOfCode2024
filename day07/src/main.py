from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable
import itertools


class Operator(StrEnum):
    ADD = '+',
    MUL = '*',
    CON = '||',


@dataclass(frozen=True)
class Equation:
    result: int
    numbers: tuple[int]

    def build(self, operators: Iterable[Operator]):
        output = self.numbers[0]
        for number, operator in zip(self.numbers[1:], operators):
            match operator:
                case Operator.ADD:
                    output += number
                case Operator.MUL:
                    output *= number
                case Operator.CON:
                    output = int(f'{output}{number}')
        return output


@dataclass
class TestCaseSet:
    raw_equations: list[Equation]
    possible_results: dict[(Equation, str), int] = None

    def evaluate(self, operators: list[Operator]):
        total = 0
        print(len(self.raw_equations))
        for i, eq in enumerate(self.raw_equations):
            print(f'eqn number {i}')
            number_components = len(eq.numbers) - 1
            for operators_ in itertools.product(operators,
                                                repeat=number_components):
                if (result := eq.build(operators_)) == eq.result:
                    total += result
                    break
        return total


def parse() -> TestCaseSet:
    with open('../input.txt') as f:
        data = [s.strip('\n') for s in f.readlines()]
    equations = []
    for row in data:
        start, nums = row.split(':')
        result = int(start.strip())
        numbers = [int(n) for n in nums.split()]
        equations.append(Equation(result, tuple(numbers)))
    return TestCaseSet(equations)


def part1():
    eqns = parse()
    print(f'Part 1: {eqns.evaluate([Operator.ADD, Operator.MUL])}')


def part2():
    eqns = parse()
    print(
        f'Part 2: {eqns.evaluate([Operator.ADD, Operator.MUL, Operator.CON])}'
    )


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
