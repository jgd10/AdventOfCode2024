from aoc import Direction, Point, parse_file, InputType, timer, TimeUnit


class MemorySpace:
    def __init__(self, byte_positions: list[Point]):
        self.byte_positions: list[Point] = byte_positions
        imax, jmax = 0, 0
        imax = max([p.x for p in byte_positions])
        jmax = max([p.y for p in byte_positions])
        self.end: Point = Point(imax, jmax)
        self.start: Point = Point(0, 0)
        self.grid = {Point(i, j) for i in range(imax+1) for j in range(jmax+1)}

    def find_shortest_path_to_end_at_time(self, t: int = 1024):
        blocks = set(self.byte_positions[:t])
        queue = []
        explored = {self.start}
        paths: dict[Point, Point] = {}
        queue.append(self.start)
        while queue:
            square = queue.pop(0)
            if square == self.end:
                return True, paths
            available_neighbors = square.immediate_neighbors - blocks
            allowed_neighbors = available_neighbors.intersection(self.grid)
            unexplored_neighbors = allowed_neighbors - explored
            for neighbor in unexplored_neighbors:
                explored.add(neighbor)
                paths[neighbor] = square
                queue.append(neighbor)
        return False, paths

    def get_path_from_dict(self, paths: dict[Point, Point]):
        path = {self.end}
        p = paths[self.end]
        while p != self.start:
            p = paths[p]
            path.add(p)
        return path

    def get_length_of_shortest_path_to_end_at_time(self, t: int = 1024):
        success, paths = self.find_shortest_path_to_end_at_time(t)
        path = self.get_path_from_dict(paths)
        return len(path)

    def find_killer_byte_after(self, t: int = 1024):
        success, paths = self.find_shortest_path_to_end_at_time(t)
        path = self.get_path_from_dict(paths)
        while success:
            t += 1
            new_byte = self.byte_positions[t-1]
            if new_byte in path:
                success, paths = self.find_shortest_path_to_end_at_time(t)
                if success:
                    path = self.get_path_from_dict(paths)
            else:
                continue
        return self.byte_positions[t-1]


def parse(input_type: InputType):
    data = parse_file(input_type)
    bytes_ = []
    for row in data:
        nums = [int(n) for n in row.split(',')]
        bytes_.append(Point(*nums))
    return MemorySpace(bytes_)

@timer(TimeUnit.ms)
def part1(input_type: InputType):
    ms = parse(input_type)
    if input_type == InputType.EXAMPLE:
        t = 12
    else:
        t = 1024
    print(f'Part 1 : {ms.get_length_of_shortest_path_to_end_at_time(t)}')

@timer(TimeUnit.s)
def part2(input_type: InputType):
    ms = parse(input_type)
    if input_type == InputType.EXAMPLE:
        t = 12
    else:
        t = 1024
    print(f'Part 2: {ms.find_killer_byte_after(t)}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    part1(InputType.INPUT)
    part2(InputType.INPUT)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
