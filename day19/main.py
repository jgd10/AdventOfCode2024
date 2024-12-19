from aoc import parse_file, InputType
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


def find_num_poss_arrangs(pattern: str, towels: tuple[str, ...], used_towels: tuple[str, ...], counter: int):
    already_used_towels = None
    @functools.cache
    def find_number_possible_arrangements(pattern: str, towels: tuple[str, ...], used_towels: tuple[str, ...], counter: int):
        if len(pattern) == 0:
            if  already_used_towels is None:
                already_used_towels = (set(used_towels),)
                counter += 1
            if used_towels not in already_used_towels:
                already_used_towels += (set(used_towels), )
                counter += 1
        for towel in towels:
            if pattern.startswith(towel):
                if used_towels is None:
                    used_towels = (towel,)
                else:
                    used_towels = used_towels + (towel,)
                counter += find_number_possible_arrangements(pattern[len(towel):], towels, used_towels, counter, already_used_towels)
        return counter
    return find_number_possible_arrangements(pattern, towels, used_towels, counter)


@dataclass
class Onsen:
    towels: list[str]
    patterns: set[str]
    _towel_cols: set[str] = None
    _towel_lens: dict[int, set[str]] = None
    _results_dict: dict[tuple[str, tuple[str, ...]]] = None
    already_used_towels: list[set[str]] = None
    cache: dict = None

    @property
    def results_dict(self):
        if self._results_dict is None:
            self._results_dict = {}
        return self._results_dict

    @property
    def towel_colours(self):
        if self._towel_cols is None:
            self._towel_cols = {s for p in self.towels for s in p}
        return self._towel_cols

    @property
    def towels_by_length(self):
        if self._towel_lens is None:
            lens = {}
            for t in set(self.towels):
                num = self.towels.count(t)
                if num not in lens:
                    lens[num] = {t}
                else:
                    lens[num].add(t)
            self._towel_lens = lens
        return self._towel_lens

    def is_pattern_possible(self, pattern: str):
        if not set(pattern).issubset(self.towel_colours):
            return False

        possible_towels = []
        for t in self.towels:
            if t in pattern:
                possible_towels.append(t)
        possible = self.remove_possible_towels(pattern, possible_towels)
        if not possible:
            print(pattern)
        return possible

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
                print(count)
                total += count
        return total

    def find_number_possible_arrangements(self,
                                          pattern: str,
                                          towels: tuple[str, ...],
                                          used_towels: tuple[str, ...],
                                          counter: int,
                                          already_used_towels: tuple[tuple[str, ...], ...]):
        key = (pattern, towels, used_towels, already_used_towels)
        if key in self.cache:
            return self.cache[key]
        if len(pattern) == 0:
            unique_towels = tuple((set(used_towels)))
            if unique_towels not in already_used_towels:
                already_used_towels += unique_towels
        for towel in towels:
            if pattern.startswith(towel):
                if used_towels is None:
                    used_towels = (towel,)
                else:
                    used_towels = used_towels + (towel,)
                already_used_towels = self.find_number_possible_arrangements(
                    pattern[len(towel):], towels, used_towels, counter,
                    already_used_towels)
        self.cache[key] = already_used_towels
        return already_used_towels


def parse(inout_type: InputType):
    data = parse_file(inout_type)
    towels = data.pop(0).split(', ')
    patterns = set()
    for row in data:
        if row:
            patterns.add(row)
    return Onsen(towels, patterns)


def part1(input_type: InputType):
    onsen = parse(input_type)
    print(f'Part 1: {onsen.find_num_possible_patterns()}')
    pass


def part2(input_type: InputType):
    onsen = parse(input_type)
    print(f'Part 2: {onsen.find_num_possible_arrangements()}')
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #part1(InputType.EXAMPLE)
    part2(InputType.INPUT)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
