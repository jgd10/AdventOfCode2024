from dataclasses import dataclass
from enum import Enum
from shapely.geometry import Polygon
import polygons


class Direction(Enum):
    N = 1
    E = 2
    W = 3
    S = 4


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def nearby_points(self) -> 'set[Point]':
        return {Point(x=self.x-1, y=self.y),
                Point(x=self.x+1, y=self.y),
                Point(x=self.x, y=self.y-1),
                Point(x=self.x, y=self.y+1)}

    def nearby_diagonals(self) -> 'set[Point]':
        return {Point(x=self.x-1, y=self.y-1),
                Point(x=self.x+1, y=self.y-1),
                Point(x=self.x-1, y=self.y+1),
                Point(x=self.x+1, y=self.y+1)}

    def nearby_points_with_direction(self) -> 'set[tuple[Point, Direction]]':
        return {(Point(x=self.x-1, y=self.y), Direction.W),
                (Point(x=self.x+1, y=self.y), Direction.E),
                (Point(x=self.x, y=self.y-1), Direction.N),
                (Point(x=self.x, y=self.y+1), Direction.S)}

@dataclass(frozen=True)
class Tile:
    point: Point
    plant: str

    def get_neighbor_tiles(self, plant: str = None) -> 'set[Tile]':
        if plant is None:
            plant = self.plant
        return {Tile(p, plant) for p in self.point.nearby_points()}


def parse():
    with open('./input.txt') as f:
        data = [[c for c in s.strip('\n')] for s in f.readlines()]
        tiles = {Tile(Point(i, j), c) for j, row in enumerate(data) for i, c in enumerate(row)}
    return Garden(tiles)


@dataclass
class Garden:
    tiles: set[Tile]
    _areas: list[set[Tile]] = None

    @property
    def areas(self):
        if self._areas is None:
            self._areas = []
        return self._areas

    def find_areas(self):
        counted = set()
        uncounted = self.tiles.copy()
        while len(self.tiles) != len(counted):
            start_tile = uncounted.pop()
            new_area = {start_tile}
            final_area = {start_tile}
            counted.add(start_tile)
            counter = 0
            while new_area:
                tile = new_area.pop()
                current_plant = tile.plant
                for neighbor in tile.point.nearby_points():
                    neighbor_tile = Tile(neighbor, current_plant)
                    if neighbor_tile in self.tiles and neighbor_tile not in counted:
                        counted.add(neighbor_tile)
                        new_area.add(neighbor_tile)
                        final_area.add(neighbor_tile)
                    else:
                        counter += 1
            uncounted -= final_area
            self.areas.append(final_area)

    def find_fencing_cost(self) -> int:
        self.find_areas()
        total = 0
        for area in self.areas:
            size = len(area)
            perimeter = 0
            for tile in area:
                neighbors = tile.get_neighbor_tiles()
                perimeter += (4 - len(neighbors.intersection(area)))
            cost = size * perimeter
            total += cost
        return total

    def find_bulk_fencing_cost(self) -> int:
        def condition(tile, previous, direction_):
            match direction_:
                case Direction.N:
                    return tile.point.y == previous.point.y and abs(tile.point.x - previous.point.x) <= 1
                case Direction.S:
                    return tile.point.y == previous.point.y and abs(tile.point.x - previous.point.x) <= 1
                case Direction.E:
                    return tile.point.x == previous.point.x and abs(tile.point.y - previous.point.y) <= 1
                case Direction.W:
                    return tile.point.x == previous.point.x and abs(tile.point.y - previous.point.y) <= 1
        self.find_areas()
        total = 0
        for area in self.areas:
            size = len(area)
            area_points = {a.point for a in area}
            all_edge_tiles = {t for t in area if len(t.point.nearby_points().intersection(area_points)) != 4}
            sides = 0
            for direction in Direction:
                direction_edge_tiles = [tile for tile in all_edge_tiles for p, d in tile.point.nearby_points_with_direction() if d == direction and p not in area_points]
                if direction in [Direction.N, Direction.S]:
                    unique_y = {t.point.y for t in direction_edge_tiles}
                    for y in unique_y:
                        sorted_tiles = [t for t in direction_edge_tiles if t.point.y == y]
                        sorted_tiles = sorted(sorted_tiles,
                                              key=lambda x: x.point.x)
                        prev = sorted_tiles[0]
                        sides += 1
                        for t in sorted_tiles:
                            if not condition(t, prev, direction):
                                sides += 1
                            prev = t
                else:
                    unique_x = {t.point.x for t in direction_edge_tiles}
                    for x in unique_x:
                        sorted_tiles = [t for t in direction_edge_tiles if
                                        t.point.x == x]
                        sorted_tiles = sorted(sorted_tiles,
                                              key=lambda x_: x_.point.y)
                        prev = sorted_tiles[0]
                        sides += 1
                        for t in sorted_tiles:
                            if not condition(t, prev, direction):
                                sides += 1
                            prev = t
            cost = size * sides
            total += cost
        return total

def part1():
    garden = parse()
    print(f'Part 1: {garden.find_fencing_cost()}')


def part2():
    garden = parse()
    print(f'Part 2: {garden.find_bulk_fencing_cost()}')


def main():
    part1()
    part2()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
