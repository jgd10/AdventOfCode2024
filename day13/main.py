import math
from dataclasses import dataclass


A_COST = 3
B_COST = 1

@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    @classmethod
    def zero(cls):
        return cls(0, 0)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return Vector(other.x - self.x, other.y - self.y)

    def __radd__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other: 'int | Vector'):
        if isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        else:
            raise NotImplementedError

    def __mod__(self, other: 'int | Vector'):
        if isinstance(other, int):
            return Vector(self.x % other, self.y % other)
        else:
            return Vector(self.x % other.x, self.y % other.y)

    def greatest_common_divisor(self, other: 'int | Vector'):
        if isinstance(other, int):
            return Vector(math.gcd(self.x, other), math.gcd(self.y, other))
        else:
            return Vector(math.gcd(self.x, other.x), math.gcd(self.y, other.y))


@dataclass
class ClawMachine:
    button_a: Vector
    button_b: Vector
    prize: Vector

    @classmethod
    def from_rows(cls, rows: list[str]):
        row1 = rows[0]
        row2 = rows[1]
        row3 = rows[2]
        row1 = row1.replace('Button A: ', '')
        row2 = row2.replace('Button B: ', '')
        row3 = row3.replace('Prize: ', '')
        row3 = row3.replace('=', '')
        vectors = []
        for row in [row1, row2, row3]:
            row = row.replace('X', '')
            row = row.replace('Y', '')
            row_nums = [int(n) for n in row.split(', ')]
            new = Vector(*row_nums)
            vectors.append(new)
        return cls(*vectors)

    def is_possible(self):
        gcd = self.button_a.greatest_common_divisor(self.button_b)
        if self.prize % gcd == Vector.zero():
            n, m = self.minimum_operations()
            if n < 0 or m < 0:
                return False
            elif not math.isclose(n, round(n), rel_tol=0, abs_tol=0.001) or not math.isclose(m, round(m), abs_tol=0.001):
                return False
            else:
                return True

    def minimum_operations(self):
        a_ratio = self.button_a.x / self.button_a.y
        m = (self.prize.y*a_ratio - self.prize.x) / (self.button_b.y*a_ratio - self.button_b.x)
        n = (self.prize.y - self.button_b.y*m) / self.button_a.y
        return n, m

    def minimum_cost(self):
        n, m = self.minimum_operations()
        print(n, m)
        n, m = round(n), round(m)
        print(n, m)
        print()
        return n*A_COST + m*B_COST


def parse():
    with open('./input.txt') as f:
        data = [s.strip('\n') for s in f.readlines()]
    machines = []
    machine = []
    for row in data:
        if row:
            machine.append(row)
        else:
            machines.append(machine)
            machine = []
    machines.append(machine)
    machines = [ClawMachine.from_rows(machine) for machine in machines]
    return machines


def part1():
    machines = parse()
    total = 0
    for machine in machines:
        if machine.is_possible():
            total += machine.minimum_cost()
    print(f'Part 1: {total}')


def part2():
    machines = parse()
    total = 0
    for machine in machines:
        machine.prize = machine.prize + Vector(10000000000000, 10000000000000)
        if machine.is_possible():
            total += machine.minimum_cost()
    print(f'Part 2: {total}')


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
