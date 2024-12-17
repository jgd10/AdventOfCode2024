from dataclasses import dataclass
from enum import Enum
import math


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


START_DIRECTION = Direction.E

@dataclass(frozen=True)
class Point:
    x: int
    y: int

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

    def neighbor_points(self, direction: Direction, score: int) -> 'set[tuple[Point, int, Direction]]':
        return {(self.point_in_direction(direction), score + 1, direction),
                (self, score + 1000, direction.rotate_clockwise()),
                (self, score + 1000, direction.rotate_anticlockwise())}


#class Reindeer(Point):
#    def __init__(self, point: Point, direction: Direction):
#        super().__init__(point.x, point.y)
#        self.direction = direction


@dataclass
class Maze:
    paths: set[Point]
    start: Point
    end: Point
    walls: set[Point]
    best_paths: dict[tuple[Point,int, Direction], set[tuple[Point, int, Direction]]] = None

    @classmethod
    def from_rows(cls, rows: list[str]):
        paths = set()
        walls = set()
        start, end = None, None
        for j, row in enumerate(rows):
            for i, c in enumerate(row):
                p = Point(i, j)
                match c:
                    case '#':
                        walls.add(p)
                    case '.':
                        paths.add(p)
                    case 'S':
                        start = p
                    case 'E':
                        end = p
        paths.add(start)
        paths.add(end)
        return cls(paths, start, end, walls)

    def find_lowest_score(self):
        queue = []
        explored = {(self.start, START_DIRECTION): 0}
        queue.append((self.start, 0, START_DIRECTION))
        paths: dict[tuple[Point, int, Direction], set[tuple[Point, int, Direction]]] = {}
        possible_scores = []
        while queue:
            prev_point = queue.pop(0)
            v, score, direction = prev_point
            if v == self.end:
                possible_scores.append(score)
                queue = [p for p in queue if p[1] <= possible_scores[-1]]
                continue
            for point in {p for p in v.neighbor_points(direction, score) if p[0] in self.paths}:
                key = (point[0], point[-1])
                if key not in explored or explored[key] >= point[1]:
                    explored[key] = point[1]
                    if point not in paths:
                        paths[point] = {prev_point}
                    else:
                        paths[point].add(prev_point)
                    queue.append(point)
        self.best_paths = paths
        return min(possible_scores)

    def visualise(self, tiles: set[Point]) -> str:
        imax = 0
        jmax = 0
        for block in self.walls:
            imax = max(imax, block.x)
            jmax = max(jmax, block.y)
        grid = [['.' for _ in range(imax + 1)] for k in range(jmax + 1)]
        for block in self.walls:
            grid[block.y][block.x] = '#'
        for box in tiles:
            grid[box.y][box.x] = 'O'
        rows = [''.join(row) for row in grid]
        string = '\n'.join(rows)
        return string

    def count_optimal_tiles(self, score: int) -> int:
        if self.best_paths is None:
            self.find_lowest_score()

        tiles = {(self.end, score, d) for d in Direction}
        best_tiles = {self.start}
        counter = 0
        string = self.visualise(best_tiles)
        with open(f'./output/step_{counter:05d}.txt', 'w') as file:
            file.write(string)
        while tiles:
            next_tiles = {t for t in tiles if t in self.best_paths}
            new_tiles = set()
            counter += 1
            for t in next_tiles:
                best_tiles.add(t[0])
                new_tiles.update(self.best_paths[t])
            tiles = new_tiles
            with open(f'./output/step_{counter:05d}.txt', 'w') as file:
                string = self.visualise(best_tiles)
                file.write(string)
        return len(best_tiles)


def parse(input_type: InputType, big_warehouse: bool = False):
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
    maze = Maze.from_rows(data)
    return maze


def part1(input_type: InputType):
    maze = parse(input_type)
    print(f'Part 1: {maze.find_lowest_score()}')

def part2(input_type: InputType):
    maze = parse(input_type)
    score = maze.find_lowest_score()
    print(f'Part 2: {maze.count_optimal_tiles(score)}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    part1(InputType.EXAMPLE4)
    part2(InputType.EXAMPLE4)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
