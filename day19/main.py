from aoc import parse_file, InputType, timer, TimeUnit
from dataclasses import dataclass
import functools


@functools.cache
def is_pattern_possible(pattern: str, towels: tuple[str, ...]):
    if len(pattern) == 0:
        return True
    possible = False
    for towel in towels:
        if pattern.startswith(towel) and not possible:
            possible = is_pattern_possible(pattern[len(towel):], towels)
    return possible


@functools.cache
def count_ways(pattern: str, towels: tuple[str, ...]) -> int:
    if len(pattern) == 0:
        return 1
    total = 0
    for towel in towels:
        if pattern.startswith(towel):
            total += count_ways(pattern[len(towel):], towels)
    return total


@dataclass
class Onsen:
    towels: list[str]
    patterns: set[str]

    def find_num_possible_patterns(self):
        counter = 0
        for p in self.patterns:
            if is_pattern_possible(p, tuple(self.towels)):
                counter += 1
        return counter

    def find_num_possible_arrangements(self):
        total = 0
        for p in self.patterns:
            if is_pattern_possible(p, tuple(self.towels)):
                count = count_ways(p, tuple(self.towels))
                total += count
        return total


def parse(inout_type: InputType):
    data = parse_file(inout_type)
    towels = data.pop(0).split(', ')
    patterns = set()
    for row in data:
        if row:
            patterns.add(row)
    return Onsen(towels, patterns)


@timer(TimeUnit.ms)
def part1(input_type: InputType):
    onsen = parse(input_type)
    print(f'Part 1: {onsen.find_num_possible_patterns()}')


@timer(TimeUnit.ms)
def part2(input_type: InputType):
    onsen = parse(input_type)
    print(f'Part 2: {onsen.find_num_possible_arrangements()}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    part1(InputType.INPUT)
    part2(InputType.INPUT)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
