from dataclasses import dataclass
from enum import Enum, unique
from unittest import case

height_map = {'0': '1',
              '1': '2',
              '2': '3',
              '3': '4',
              '4': '5',
              '5': '6',
              '6': '7',
              '7': '8',
              '8': '9',}

class Direction(Enum):
    N = 1
    E = 2
    W = 3
    S = 4

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_adjacent_point(self, direction: Direction) -> 'Point':
        match direction:
            case Direction.N:
                return Point(self.x, self.y - 1)
            case Direction.E:
                return Point(self.x + 1, self.y)
            case Direction.W:
                return Point(self.x - 1, self.y)
            case Direction.S:
                return Point(self.x, self.y + 1)

    def get_all_adjacent_points(self) -> set['Point']:
        return {self.get_adjacent_point(d) for d in Direction}


@dataclass(frozen=True)
class Tile:
    point: Point
    height: str

    def __repr__(self) -> str:
        return f'x:{self.point.x}-y:{self.point.y}-h:{self.height}'

    def get_possible_adjacent_tiles(self):
        if self.height != '9':
            return {Tile(p, height_map[self.height])
                    for p in self.point.get_all_adjacent_points()}
        else:
            return set()


class InputType(Enum):
    EXAMPLE=1
    INPUT=2
    EXAMPLE1=3
    EXAMPLE2=4
    EXAMPLE3=5


@dataclass
class HikingMap:
    tiles: set[Tile]
    _points: dict[Point, Tile] = None

    @property
    def points(self) -> dict[Point, Tile]:
        if self._points is None:
            self._points = {t.point: t for t in self.tiles}
        return self._points

    def find_shortest_paths(self, start_height: str, end_height: str):
        starting_tiles = {t for t in self.tiles if t.height == start_height}
        total = 0
        for tile in starting_tiles:
            end_points = self.bfs(tile, end_height)
            total += len(end_points)
        return total

    def bfs(self, start: Tile, end_height: str) -> set[Tile]:
        explored: set[Tile] = {start}
        queue: set[Tile] = {start}
        end_points: set[Tile] = set()
        while len(queue) > 0:
            v = queue.pop()
            if v.height == end_height:
                end_points.add(v)
            for neighbor in v.get_possible_adjacent_tiles():
                if neighbor in self.tiles and neighbor not in explored:
                    explored.add(neighbor)
                    queue.add(neighbor)
        return end_points

    def bfs2(self, start: Tile, end_height: str) -> tuple[set[Tile], list[list[Tile]]]:
        explored: set[Tile] = {start}
        queue: set[Tile] = {start}
        end_points: set[Tile] = set()
        trails = [[start]]
        while len(queue) > 0:
            v = queue.pop()
            if v.height == end_height:
                end_points.add(v)
            neighbors = []
            for neighbor in v.get_possible_adjacent_tiles():
                if neighbor in self.tiles:
                    neighbors.append(neighbor)
                    explored.add(neighbor)
                    queue.add(neighbor)
            if neighbors:
                trails = [trail + [neighbor] if trail[-1] == v else trail for neighbor in neighbors for trail in trails]
        return end_points, trails

    def get_trailhead_ratings(self, plot: bool = False):
        starting_tiles = {t for t in self.tiles if t.height == '0'}
        # starting_tiles = {Tile(Point(x=1, y=7), '0')}
        total = 0
        all_trails = []
        for tile in starting_tiles:
            end_points, trails = self.bfs2(tile, '9')
            trails = [t for t in trails]
            unique_ = []
            for trail in trails:
                if trail not in unique_ and any([t.height=='9' for t in trail]):
                    unique_.append(trail)
            total += len(unique_)
            all_trails.extend(unique_)
        if plot:
            self.make_plots(all_trails)
        return total

    def make_plots(self, trails: list[list[Tile]]):
        counter = 0
        for trail in trails:
            marked_points = set()
            for tile in trail:
                marked_points.add(tile.point)
                self.output_input_map(marked_points, counter)
                counter += 1

    def output_input_map(self, marked_points: set[Point], id_: int) -> None:
        xmax = max({t.point.x for t in self.tiles})
        ymax = max({t.point.y for t in self.tiles})
        data = [['.' for __ in range(xmax)] for _ in range(ymax)]
        for i in range(xmax):
            for j in range(ymax):
                p = Point(i, j)
                tile = self.points[p]
                if p in marked_points:
                    data[j][i] = '#'
                else:
                    data[j][i] = tile.height
        rows = [''.join(row) for row in data]
        string = '\n'.join(rows)
        with open(f'../visualisation/output_part2_{id_:05}.txt', 'w', encoding='utf-8') as f:
            f.write(string)



def parse(input_type: InputType):
    match input_type:
        case InputType.EXAMPLE:
            filepath = '../example.txt'
        case InputType.INPUT:
            filepath = '../input.txt'
        case InputType.EXAMPLE1:
            filepath = '../example1.txt'
        case InputType.EXAMPLE2:
            filepath = '../example2.txt'
        case InputType.EXAMPLE3:
            filepath = '../example3.txt'
        case _:
            raise TypeError('Invalid input type')

    with open(filepath) as f:
        data = [[c for c in s.strip('\n')] for s in f.readlines()]

    tiles = {Tile(Point(i, j), c)
             for j, row in enumerate(data)
             for i, c in enumerate(row) if c != '.'}
    return HikingMap(tiles)


def part1():
    hiking_map = parse(InputType.INPUT)
    print(f'Part 1: {hiking_map.find_shortest_paths('0', '9')}')


def part2():
    hiking_map = parse(InputType.INPUT)
    print(f'Part 2: {hiking_map.get_trailhead_ratings(plot=True)}')


def main():
    part1()
    part2()

if __name__ == '__main__':
    main()
