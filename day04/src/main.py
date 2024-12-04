from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


class Letter(Enum):
    X = 0
    M = 1
    A = 2
    S = 3


@dataclass(frozen=True)
class Coordinate:
    i: int
    j: int

    @property
    def cross_neighbours(self):
        return {(Coordinate(self.i-1, self.j-1), Direction.NW),
                (Coordinate(self.i+1, self.j-1), Direction.NE),
                (Coordinate(self.i-1, self.j+1), Direction.SW),
                (Coordinate(self.i+1, self.j+1), Direction.SE),}

    @property
    def neighbouring_points(self):
        return {Coordinate(self.i - 1, self.j),
                Coordinate(self.i - 1, self.j - 1),
                Coordinate(self.i - 1, self.j + 1),
                Coordinate(self.i, self.j - 1),
                Coordinate(self.i, self.j + 1),
                Coordinate(self.i + 1, self.j),
                Coordinate(self.i + 1, self.j - 1),
                Coordinate(self.i + 1, self.j + 1)}

    @property
    def neighbouring_points_with_direction(self):
        return {(Coordinate(self.i - 1, self.j), Direction.W),
                (Coordinate(self.i - 1, self.j - 1), Direction.NW),
                (Coordinate(self.i - 1, self.j + 1), Direction.SW),
                (Coordinate(self.i, self.j - 1), Direction.N),
                (Coordinate(self.i, self.j + 1), Direction.S),
                (Coordinate(self.i + 1, self.j), Direction.E),
                (Coordinate(self.i + 1, self.j - 1), Direction.NE),
                (Coordinate(self.i + 1, self.j + 1), Direction.SE)}


class InputType(Enum):
    EXAMPLE = 0
    INPUT = 1


@dataclass
class WordSearch:
    coordinates: dict[Coordinate, Letter]
    imax: int
    jmax: int

    def find_all_cross_mas(self):
        counter = 0
        for c, v in self.coordinates.items():
            if v == Letter.A:
                cross_neighbours = [d for d in c.cross_neighbours if d[0] in self.coordinates]
                if len(cross_neighbours) != 4:
                    continue
                letters = [self.coordinates[n[0]] for n in cross_neighbours]
                if set(letters) != {Letter.M, Letter.S}:
                    continue
                if letters.count(Letter.M) != 2 \
                        or letters.count(Letter.S) != 2:
                    continue
                letter_directions = {d[1]: self.coordinates[d[0]] for d in cross_neighbours}
                if letter_directions[Direction.NW] == letter_directions[Direction.SE] \
                    or letter_directions[Direction.SW] == letter_directions[Direction.NE]:
                    continue
                counter += 1
        return counter

    def find_xmas(self):
        def find_next_letter(coords, letter):
            new_coords = []
            next_letter = None
            for c, direction in coords:
                neighbours = [m for m in c.neighbouring_points_with_direction if
                              m[0] in self.coordinates
                              and m[1] == direction
                              and self.coordinates[m[0]] == letter]
                new_coords.extend(neighbours)
            if letter == Letter.S:
                return len(new_coords)
            else:
                match letter:
                    case Letter.X:
                        next_letter = Letter.M
                    case Letter.M:
                        next_letter = Letter.A
                    case Letter.A:
                        next_letter = Letter.S
                    case Letter.S:
                        raise ValueError()
                return find_next_letter(new_coords, next_letter)

        available_directions = {Direction.S, Direction.N, Direction.W, Direction.E,
                                Direction.SE, Direction.SW, Direction.NW, Direction.NE}
        xes = [(c, d) for c, v in self.coordinates.items() if v == Letter.X for d in available_directions]
        return find_next_letter(xes, Letter.M)


def parse(input_type: InputType) -> WordSearch:
    match input_type:
        case InputType.EXAMPLE:
            filename = '../example.txt'
        case InputType.INPUT:
            filename = '../input.txt'
        case _:
            raise ValueError()
    with open(filename) as f:
        data = [s.strip('\n') for s in f.readlines()]
    coordinates = {}
    imax, jmax = 0, 0
    for j, row in enumerate(data):
        for i, character in enumerate(row):
            imax = max(imax, i)
            jmax = max(jmax, j)
            match character:
                case 'X':
                    new = Letter.X
                case 'M':
                    new = Letter.M
                case 'A':
                    new = Letter.A
                case 'S':
                    new = Letter.S
                case _:
                    raise ValueError()
            coordinates[Coordinate(i, j)] = new
    return WordSearch(coordinates, imax, jmax)


def part1():
    ws = parse(InputType.EXAMPLE)
    print(f'Part 1: {ws.find_xmas()}')


def part2():
    ws = parse(InputType.INPUT)
    print(f'Part 2: {ws.find_all_cross_mas()}')


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
