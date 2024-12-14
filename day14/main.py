from dataclasses import dataclass
from enum import Enum


class InputType(Enum):
    INPUT = 0,
    EXAMPLE = 1,


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

class Position(Vector):
    def __init__(self, x: int, y: int):
        super().__init__(x,y)

    @property
    def tree_neighbors(self):
        return {Position(self.x, self.y-1),
                Position(self.x, self.y-2),
                Position(self.x, self.y-3),
                Position(self.x-2, self.y-1),
                Position(self.x+2, self.y-1),
                Position(self.x-1, self.y-2),
                Position(self.x+1, self.y-2)}


class Velocity(Vector):
    def __init__(self, x: int, y: int):
        super().__init__(x,y)


@dataclass(frozen=True)
class Robot:
    position: Position
    velocity: Velocity

    @classmethod
    def from_str(cls, string: str):
        """p=4,11 v=-61,-65"""
        pos, vel = string.split(' ')
        pos = pos.replace('p=', '')
        vel = vel.replace('v=', '')
        px, py = pos.split(',')
        vx, vy = vel.split(',')
        position = Position(int(px), int(py))
        velocity = Velocity(int(vx), int(vy))
        return cls(position, velocity)

    def get_position_after(self, time: int, grid: Vector) -> Vector:
        delta_x = self.velocity.x * time
        delta_y = self.velocity.y * time
        new_x = (abs(delta_x) % grid.x)*(delta_x//abs(delta_x)) + self.position.x
        new_y = (abs(delta_y) % grid.y)*(delta_y//abs(delta_y)) + self.position.y
        if new_x >= grid.x:
            new_x = new_x - grid.x
        if new_y >= grid.y:
            new_y = new_y - grid.y
        if new_x < 0:
            new_x = new_x + grid.x
        if new_y < 0:
            new_y = new_y + grid.y
        return Position(new_x, new_y)


@dataclass
class Security:
    robots: set[Robot]
    input_type: InputType
    _grid: Vector = None

    @property
    def grid(self) -> Vector:
        if self._grid is None:
            if self.input_type == InputType.INPUT:
                self._grid = Vector(101, 103)
            else:
                self._grid = Vector(11, 7)
        return self._grid

    def visualise(self, time: int):
        result = self.elapse_time(time)
        grid = [['.' for c in range(self.grid.x)] for r in range(self.grid.y)]
        for pos, value in result.items():
            grid[pos.y][pos.x] = str(value)
        rows = [''.join(row) for row in grid] + [f't = {time}s', '']
        string = '\n'.join(rows)
        print(string)

    def elapse_time(self, time: int):
        new_positions = [r.get_position_after(time, self.grid) for r in self.robots]
        positions_counts = {}
        for position in new_positions:
            if position not in positions_counts:
                positions_counts[position] = 1
            else:
                positions_counts[position] += 1
        return positions_counts

    def find_tree(self):
        time = 1
        tree = False
        while not tree:
            positions = {p for p in self.elapse_time(time).keys()}
            time += 1
            tree = any({p.tree_neighbors.issubset(positions) for p in positions})
        self.visualise(time)
        print(time)

    def get_safety_factor_after(self, time: int):
        positions = self.elapse_time(time)
        north_west = 0
        north_east = 0
        south_west = 0
        south_east = 0
        x_boundary = self.grid.x // 2
        y_boundary = self.grid.y // 2
        for position, count in positions.items():
            if position.x < x_boundary and position.y < y_boundary:
                north_west += count
            elif position.x > x_boundary and position.y > y_boundary:
                south_east += count
            elif position.x < x_boundary and position.y > y_boundary:
                south_west += count
            elif position.x > x_boundary and position.y < y_boundary:
                north_east += count
            else:
                pass
        print(north_west, north_east, south_west, south_east)
        return north_west * north_east * south_west * south_east


def parse(input_type: InputType):
    match input_type:
        case InputType.INPUT:
            filepath = './input.txt'
        case InputType.EXAMPLE:
            filepath = './example.txt'
        case _:
            raise ValueError

    with open(filepath) as f:
        data = [s.strip('\n') for s in f.readlines()]
    robots = {Robot.from_str(s) for s in data}
    return Security(robots, input_type=input_type)


def part1(input_type: InputType):
    security = parse(input_type)
    #security.visualise(100)
    safety_factor = security.get_safety_factor_after(100)
    print(f'Part 1: {safety_factor}')


def part2(input_type: InputType):
    security = parse(input_type)
    security.visualise(7051)
    #security.find_tree()
    #safety_factor = security.get_safety_factor_after(100)
    #print(f'Part 2: {safety_factor}')

def main():
    part1(InputType.INPUT)
    part2(InputType.INPUT)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
