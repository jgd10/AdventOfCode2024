import math
import pathlib
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from time import time


class TimeUnit(Enum):
    s = 1
    ms = 2
    us = 3
    min = 4
    hr = 5


# Based on https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
def timer(unit: TimeUnit = TimeUnit.s):
    def timing(f):
        @wraps(f)
        def wrap(*args, **kw):
            ts = time()
            result = f(*args, **kw)
            te = time()
            time_string = ''
            match unit:
                case TimeUnit.s:
                    time_string = f'{te - ts:.4f} s'
                case TimeUnit.ms:
                    time_string = f'{1000*(te - ts):.4f} ms'
                case TimeUnit.us:
                    time_string = f'{1000000*(te - ts):.4f} us'
                case TimeUnit.min:
                    time_string = f'{(te - ts)/60.:.4f} min'
                case TimeUnit.hr:
                    time_string = f'{(te - ts)/3600.:.4f} hr'
                case _:
                    ValueError
            print(f'func:{f.__name__} args:{args}{kw} took: {time_string}')
            return result
        return wrap
    return timing


class InputType(Enum):
    INPUT = 0,
    EXAMPLE = 1,
    EXAMPLE2 = 2,
    EXAMPLE3 = 3,
    EXAMPLE4 = 4,


class Direction(Enum):
    N = 1
    E = 2
    W = 3
    S = 4

    def rotate_clockwise(self):
        match self:
            case Direction.N:
                return Direction.E
            case Direction.E:
                return Direction.S
            case Direction.S:
                return Direction.W
            case Direction.W:
                return Direction.N

    def rotate_anticlockwise(self):
        match self:
            case Direction.N:
                return Direction.W
            case Direction.E:
                return Direction.N
            case Direction.S:
                return Direction.E
            case Direction.W:
                return Direction.S


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def diff(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y)

    @property
    def length(self):
        return abs(self.x) + abs(self.y)

    def point_in_direction(self, direction: Direction) -> 'Point':
        match direction:
            case Direction.N:
                return Point(self.x, self.y-1)
            case Direction.E:
                return Point(self.x+1, self.y)
            case Direction.W:
                return Point(self.x-1, self.y)
            case Direction.S:
                return Point(self.x, self.y+1)

    @property
    def size(self):
        return int(math.sqrt(self.x**2 + self.y**2))

    @property
    def immediate_neighbors(self):
        return {Point(self.x, self.y-1),
                Point(self.x, self.y+1),
                Point(self.x-1, self.y),
                Point(self.x+1, self.y)}

    def immediate_neighbors_after(self, steps: int):
        step = 1
        results = self.immediate_neighbors
        while step < steps:
            new = set()
            for p in results:
                new.update(p.immediate_neighbors)
            results = new
            step += 1
        return new


    @property
    def diagonal_neighbors(self):
        return {Point(self.x + 1, self.y - 1),
                Point(self.x + 1, self.y + 1),
                Point(self.x - 1, self.y - 1),
                Point(self.x - 1, self.y + 1)}

    @property
    def all_neighbors(self):
        new = set()
        new.update(self.immediate_neighbors)
        new.update(self.diagonal_neighbors)
        return new


def parse_file(input_type: InputType):
    match input_type:
        case InputType.INPUT:
            filepath = './input.txt'
        case InputType.EXAMPLE:
            filepath = './example.txt'
        case InputType.EXAMPLE2:
            filepath = './example2.txt'
        case InputType.EXAMPLE3:
            filepath = './example3.txt'
        case InputType.EXAMPLE4:
            filepath = './example4.txt'
        case _:
            raise ValueError

    with open(filepath) as f:
        data = [s.strip('\n') for s in f.readlines()]

    return data

class Direction8(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


def get_last_index(a: list | tuple) -> int:
  for i, e in enumerate(reversed(a)):
    if e is not None:
      return len(a) - i - 1
  return -1


def scalar_digit_multiply(number: tuple[int, ...], digit: int):
    result = []
    carry = 0
    for n in reversed(number):
        ans = str(n * digit + carry)
        if len(ans) > 1:
            carry = int(ans[:-1])
            ans = ans[-1]
        else:
            carry = 0
        result.insert(0, int(ans))
    if carry > 0:
        result.insert(0, carry)
    return result


def long_sum(data: list[list[int]]) -> tuple[int, ...]:
    carry = 0
    result = []
    while any([len(row) > 0 for row in data]):
        total = sum([row.pop() for row in data if len(row) > 0])
        ans = str(total + carry)
        if len(ans) > 1:
            carry = int(ans[:-1])
            ans = ans[-1]
        else:
            carry = 0
        result.insert(0, int(ans))
    if carry > 0:
        result.insert(0, carry)
    return tuple(result)


def long_multiply(num1: tuple[int, ...], num2: tuple[int, ...]) -> tuple[int, ...]:
    """Long multiplication.

    Equivalent to,

        num1
    x   num2
    --------
    ........
    --------

    :param num1:
    :param num2:
    :return:
    """
    results = []
    for i, n in enumerate(reversed(num2)):
        result = scalar_digit_multiply(num1, n)
        result.extend([0 for _ in range(i)])
        results.append(result)

    return long_sum(results)


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
            return Vector(math.gcd(self.x, other),
                          math.gcd(self.y, other))
        else:
            return Vector(math.gcd(self.x, other.x),
                          math.gcd(self.y, other.y))


def visualise(points: dict[Point, str], filepath: pathlib.Path = None,
              print_: bool = False):
    xmax = max({p.x for p in points})
    ymax = max({p.y for p in points})
    data = [['.' for __ in range(xmax)] for _ in range(ymax)]
    for i in range(xmax):
        for j in range(ymax):
            p = Point(i, j)
            string = points[p]
            data[j][i] = string
    rows = [''.join(row) for row in data]
    string = '\n'.join(rows)
    if print_ is True:
        print(string)
    if filepath is not None:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(string)
