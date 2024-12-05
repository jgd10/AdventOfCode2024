from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    first: int
    last: int


@dataclass
class Update:
    pages: list[int]

    def is_correct(self, rules: list[Rule]):
        for rule in rules:
            if not self.rule_followed(rule):
                return False
        return True

    def force_rule(self, rule: Rule):
        i1, i2 = self.pages.index(rule.first), self.pages.index(rule.last)
        self.pages[i2], self.pages[i1] = self.pages[i1], self.pages[i2]

        #before, after = self.split_at_value(rule.first)
        #if rule.last not in after:
        #    before.remove(rule.last)
        #    after.insert(0, rule.last)
        #    self.pages = before + [rule.first] + after
        #before, after = self.split_at_value(rule.last)
        #if rule.first not in after:
        #    after.remove(rule.first)
        #    before.append(rule.first)
        #    self.pages = before + [rule.last] + after
        assert self.rule_followed(rule)

    def get_broken_rules(self, rules: list[Rule]) -> list[Rule]:
        return [r for r in rules if not self.rule_followed(r)]

    def rule_applies(self, rule: Rule):
        return rule.first in self.pages and rule.last in self.pages

    def rule_followed(self, rule: Rule) -> bool:
        if not self.rule_applies(rule):
            return True
        _, after = self.split_at_value(rule.first)
        if rule.last not in after:
            return False
        before, _ = self.split_at_value(rule.last)
        if rule.first not in before:
            return False
        return True

    def split_at_value(self, value: int) -> tuple[list[int], list[int]]:
        if value in self.pages:
            index = self.pages.index(value)
            return self.pages[:index], self.pages[index+1:]
        else:
            raise ValueError()

    def get_middle_element(self) -> int:
        n = len(self.pages)
        index = n//2
        return self.pages[index]


@dataclass
class Protocol:
    rules: list[Rule]
    updates: list[Update]

    def part1(self):
        total = 0
        for update in self.updates:
            if update.is_correct(self.rules):
                total += update.get_middle_element()
        return total

    def part2(self):
        correct, incorrect = self.sort_updates()
        return self.fix_incorrect_updates(incorrect)

    def sort_updates(self) -> tuple[list[Update], list[Update]]:
        correct, incorrect = [], []
        for update in self.updates:
            if update.is_correct(self.rules):
                correct.append(update)
            else:
                incorrect.append(update)
        return correct, incorrect

    def fix_incorrect_updates(self, incorrect: list[Update]):
        for update in incorrect:
            broken_rules = update.get_broken_rules(self.rules)
            while broken_rules:
                for rule in broken_rules:
                    if not update.rule_followed(rule):
                        update.force_rule(rule)
                broken_rules = update.get_broken_rules(self.rules)
        _, broken = self.sort_updates()
        assert len(broken) == 0
        return sum([u.get_middle_element() for u in incorrect])

class InputType(Enum):
    EXAMPLE = 0
    INPUT = 1


def parse(input_type: InputType) -> Protocol:
    match input_type:
        case InputType.EXAMPLE:
            filename = '../example.txt'
        case InputType.INPUT:
            filename = '../input.txt'
        case _:
            raise ValueError()
    with open(filename) as f:
        data = [s.strip('\n') for s in f.readlines()]
    rules = []
    updates = []
    for row in data:
        if '|' in row:
            first, last = row.split('|')
            rules.append(Rule(int(first), int(last)))
        if ',' in row:
            elems = row.split(',')
            pages = [int(e) for e in elems]
            updates.append(Update(pages))
    return Protocol(rules, updates)



def part1():
    protocol = parse(InputType.INPUT)
    print(f'Part 1: {protocol.part1()}')


def part2():
    protocol = parse(InputType.INPUT)
    print(f'Part 2: {protocol.part2()}')


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()