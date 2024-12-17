from dataclasses import dataclass
from enum import Enum


class InputType(Enum):
    INPUT = 0,
    EXAMPLE = 1,
    EXAMPLE2 = 2,
    EXAMPLE3 = 3,


class Direction(Enum):
    N = 1
    E = 2
    W = 3
    S = 4


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

    def big_boxes_in_direction(self, direction: Direction) -> 'set[BigBox]':
        match direction:
            case Direction.N:
                return {BigBox((Point(self.x-1, self.y-1),
                                Point(self.x, self.y-1))),
                        BigBox((Point(self.x, self.y - 1),
                                Point(self.x + 1, self.y - 1)))}
            case Direction.E:
                return {BigBox((Point(self.x + 1, self.y), Point(self.x + 2, self.y)))}
            case Direction.W:
                return {BigBox((Point(self.x - 2, self.y), Point(self.x - 1, self.y)))}
            case Direction.S:
                return {BigBox((Point(self.x - 1, self.y + 1),
                                Point(self.x, self.y + 1))),
                        BigBox((Point(self.x, self.y + 1),
                                Point(self.x + 1, self.y + 1)))}


@dataclass(frozen=True)
class BigBox:
    points: tuple[Point, Point]

    def box_in_lateral_direction(self, direction: Direction) -> 'BigBox':
        match direction:
            case Direction.E:
                return BigBox((Point(self.points[0].x+2, self.points[0].y), Point(self.points[1].x+2, self.points[1].y)))
            case Direction.W:
                return BigBox((Point(self.points[0].x-2, self.points[0].y), Point(self.points[1].x-2, self.points[1].y)))

    def move_box_in_lateral_direction(self, direction: Direction) -> 'BigBox':
        match direction:
            case Direction.E:
                return BigBox((Point(self.points[0].x+1, self.points[0].y), Point(self.points[1].x+1, self.points[1].y)))
            case Direction.W:
                return BigBox((Point(self.points[0].x-1, self.points[0].y), Point(self.points[1].x-1, self.points[1].y)))


    def box_in_vertical_direction(self, direction: Direction) -> 'BigBox':
        match direction:
            case Direction.N:
                return BigBox((Point(self.points[0].x, self.points[0].y-1), Point(self.points[1].x, self.points[1].y-1)))
            case Direction.S:
                return BigBox((Point(self.points[0].x, self.points[0].y+1), Point(self.points[1].x, self.points[1].y+1)))

    def possible_boxes_vertically(self, direction: Direction) -> set['BigBox']:
        boxes = {self.box_in_vertical_direction(direction)}
        match direction:
            case Direction.N:
                boxes.update({
                    BigBox((Point(self.points[0].x - 1, self.points[0].y - 1),
                            Point(self.points[1].x - 1, self.points[1].y - 1))),
                    BigBox((Point(self.points[0].x + 1, self.points[0].y - 1),
                            Point(self.points[1].x + 1, self.points[1].y - 1)))})
            case Direction.S:
                boxes.update({
                    BigBox((Point(self.points[0].x - 1, self.points[0].y + 1),
                            Point(self.points[1].x - 1, self.points[1].y + 1))),
                    BigBox((Point(self.points[0].x + 1, self.points[0].y + 1),
                            Point(self.points[1].x + 1, self.points[1].y + 1)))})
        return boxes

class Warehouse:
    blocks: set[Point]
    boxes: set[Point]
    robot: Point

    @classmethod
    def from_rows(cls, rows: list[str]) -> 'Warehouse':
        robot = None
        blocks = set()
        boxes = set()
        for j, row in enumerate(rows):
            for i, c in enumerate(row):
                p = Point(i, j)
                match c:
                    case '#':
                        blocks.add(p)
                    case 'O':
                        boxes.add(p)
                    case '@':
                        robot = Point(i, j)
        return cls(blocks, boxes, robot)

    def visualise(self):
        imax = 0
        jmax = 0
        for block in self.blocks:
            imax = max(imax, block.x)
            jmax = max(jmax, block.y)
        grid = [['.' for _ in range(imax+1)] for k in range(jmax+1)]
        for block in self.blocks:
            grid[block.y][block.x] = '#'
        for box in self.boxes:
            grid[box.y][box.x] = 'O'
        grid[self.robot.y][self.robot.x] = '@'
        rows = [''.join(row) for row in grid]
        string = '\n'.join(rows)
        return string


    def move_robot(self, direction: Direction) -> bool:
        new_point = self.robot.point_in_direction(direction)

        if new_point in self.boxes:
            next_box = new_point
            while next_box in self.boxes:
                next_box = next_box.point_in_direction(direction)
                if next_box in self.blocks:
                    return False
                elif next_box not in self.boxes:
                    self.boxes.add(next_box)
                    self.boxes.remove(new_point)
                    break
                else:
                    pass

        if new_point in self.blocks:
            return False
        self.robot = new_point
        return True

    def apply_sequence_of_moves(self, moves: list[Direction]) -> None:
        for move in moves:
            self.move_robot(direction=move)

    def calculate_gps_score(self):
        total = 0
        for box in self.boxes:
            total += box.x + box.y * 100
        return total


@dataclass
class BigWarehouse:
    blocks: set[Point]
    boxes: set[BigBox]
    robot: Point

    @classmethod
    def from_rows(cls, rows: list[str]) -> 'BigWarehouse':
        robot = None
        blocks = set()
        boxes = set()
        for j, row in enumerate(rows):
            for i, c in enumerate(row):
                p = Point(i, j)
                match c:
                    case '#':
                        blocks.add(p)
                    case '[':
                        boxes.add(BigBox((Point(i, j), Point(i+1, j))))
                    case '@':
                        robot = Point(i, j)
        return cls(blocks, boxes, robot)

    def visualise(self):
        imax = 0
        jmax = 0
        for block in self.blocks:
            imax = max(imax, block.x)
            jmax = max(jmax, block.y)
        grid = [['.' for _ in range(imax+1)] for k in range(jmax+1)]
        for block in self.blocks:
            grid[block.y][block.x] = '#'
        for big_box in self.boxes:
            grid[big_box.points[0].y][big_box.points[0].x] = '['
            grid[big_box.points[1].y][big_box.points[1].x] = ']'
        grid[self.robot.y][self.robot.x] = '@'
        rows = [''.join(row) for row in grid]
        string = '\n'.join(rows)
        return string

    def move_robot(self, direction: Direction) -> bool:
        if direction in [Direction.W, Direction.E]:
            return self.move_robot_laterally(direction=direction)
        else:
            return self.move_robot_vertically(direction=direction)

    def move_robot_laterally(self, direction: Direction) -> bool:
        new_robot_point = self.robot.point_in_direction(direction)
        box_in_way = {b for b in self.boxes if new_robot_point in b.points}
        affected_boxes = set()
        if new_robot_point in self.blocks:
            return False
        while box_in_way:
            current_box = box_in_way.pop()
            affected_boxes.add(current_box)
            match direction:
                case Direction.W:
                    new_point = current_box.points[0].point_in_direction(direction)
                case Direction.E:
                    new_point = current_box.points[1].point_in_direction(
                        direction)
                case _:
                    raise ValueError
            if new_point in self.blocks:
                return False
            box_in_way = {b for b in self.boxes if new_point in b.points}

        new_boxes = {a.move_box_in_lateral_direction(direction) for a in
                     affected_boxes}
        self.boxes -= affected_boxes
        self.boxes.update(new_boxes)
        self.robot = new_robot_point
        return True

    def move_robot_vertically(self, direction: Direction) -> bool:
        new_point = self.robot.point_in_direction(direction)
        affected_boxes = set()
        possible_boxes = self.robot.big_boxes_in_direction(direction)
        boxes = possible_boxes.intersection(self.boxes)
        while boxes and not {p for b in boxes for p in b.points}.intersection(self.blocks):
            affected_boxes.update(boxes)
            possible_boxes = set()
            for b in boxes:
                possible_boxes.update(b.possible_boxes_vertically(direction))
            pure_vertical_box_points = {p for b in boxes for p in b.box_in_vertical_direction(direction).points}
            if pure_vertical_box_points.intersection(self.blocks):
                return False
            boxes = possible_boxes.intersection(self.boxes)
        new_boxes = {a.box_in_vertical_direction(direction) for a in affected_boxes}
        self.boxes -= affected_boxes
        self.boxes.update(new_boxes)
        if new_point in self.blocks:
            return False
        self.robot = new_point
        return True

    def apply_sequence_of_moves(self, moves: list[Direction]) -> None:

        for i, move in enumerate(moves):
            result = self.visualise() + '\n' + f'{i} - Next move: {move}\n'
            with open(f'./output_results/input_output{i:05}.txt', 'w') as f:
                f.write(result)
            self.move_robot(direction=move)

    def calculate_gps_score(self):
        total = 0
        for box in self.boxes:
            total += box.points[0].x + box.points[0].y * 100
        return total


def parse_moves(string):
    directions = []
    for c in string:
        match c:
            case '^':
                d = Direction.N
            case '>':
                d = Direction.E
            case '<':
                d = Direction.W
            case 'v':
                d = Direction.S
            case _:
                raise ValueError
        directions.append(d)
    return directions


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
        case _:
            raise ValueError

    with open(filepath) as f:
        data = [s.strip('\n') for s in f.readlines()]
        warehouse = [s for s in data if '#' in s]
        moves = [s for s in data if set('<^>v').intersection(set(s))]
        all_moves = ''.join(moves)

    if big_warehouse:
        data = []
        for row_ in warehouse:
            row = []
            for c in row_:
                match c:
                    case '@':
                        row.append('@.')
                    case '#' | '.':
                        row.append(c*2)
                    case 'O':
                        row.append('[]')
                    case _:
                        raise ValueError
            data.append(row)
        warehouse = [''.join(row) for row in data]
        w = BigWarehouse.from_rows(warehouse)
    else:
        w = Warehouse.from_rows(warehouse)
    return w, parse_moves(all_moves)

def part1(input_type: InputType):
    warehouse, moves = parse(input_type)
    warehouse.apply_sequence_of_moves(moves)

    print(f'Part 1: {warehouse.calculate_gps_score()}')


def part2(input_type: InputType):
    warehouse, moves = parse(input_type, big_warehouse=True)
    print(warehouse.visualise())
    warehouse.apply_sequence_of_moves(moves)
    print(warehouse.visualise())
    print(f'Part 2: {warehouse.calculate_gps_score()}')

def main():
    #part1(InputType.INPUT)
    part2(InputType.INPUT)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

