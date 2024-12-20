from aoc import parse_file, InputType, timer, TimeUnit, Point, visualise
from dataclasses import dataclass


@dataclass(frozen=True)
class Cheat:
    coord1: Point
    coord2: Point
    saving: int
    time: int


@dataclass(frozen=True)
class CheatPair:
    coord1: Point
    coord2: Point


@dataclass
class RaceTrack:
    obstacles: set[Point]
    track: list[Point]
    start: Point
    end: Point

    @property
    def max_duration(self):
        return len(self.track)

    def find_cheats(self, cheat_time: int = 2):
        cheats = {}
        track_set = set(self.track)
        length = self.max_duration
        for t, point in enumerate(self.track):
            if t % 10 == 0:
                print(f'Track completion {t}/{length}')
            steps = 2
            while steps <= cheat_time:
                cheat_potentials = point.immediate_neighbors_after(steps=steps)
                possibilities = cheat_potentials.intersection(set(self.track[t+steps+1:]))
                for possibility in possibilities:
                    index = self.track.index(possibility)
                    saving = index - t - steps
                    cheat = Cheat(point,
                                  possibility,
                                  saving,
                                  t)
                    pair = CheatPair(point, possibility)
                    if pair in cheats:
                        cheats[pair] = cheat if cheat.saving > cheats[
                            pair].saving else cheats[pair]
                    else:
                        cheats[pair] = cheat
                steps += 1
        return cheats

    def visualise(self, cheats: list[Cheat]):
        all_points = self.obstacles.union(set(self.track))
        char_map = {}
        for p in all_points:
            if p in self.track:
                c = '.'
            if p in self.obstacles:
                c = '#'
            if p == self.start:
                c = 'S'
            if p == self.end:
                c = 'E'
            for cheat in cheats:
                if p == cheat.coord1:
                    c = '0'
                if p == cheat.coord2:
                    c = '2'
            char_map[p] = c
        visualise(char_map, print_=True)
        print()


def parse(input_type: InputType):
    obstacles = set()
    track = set()
    start = None
    end = None
    data = parse_file(input_type)
    for j, row in enumerate(data):
        for i, c in enumerate(row):
            p = Point(i, j)
            match c:
                case '#':
                    obstacles.add(p)
                case '.':
                    track.add(p)
                case 'S':
                    start = p
                    track.add(p)
                case 'E':
                    end = p
                    track.add(p)
                case _:
                    raise ValueError
    course = [start]
    square = start
    while square != end:
        squares = square.immediate_neighbors.intersection(track) - set(course)#
        assert len(squares) <= 1
        square = squares.pop()
        course.append(square)
    return RaceTrack(obstacles, course, start, end)


@timer(TimeUnit.s)
def part1(input_type: InputType):
    rt = parse(input_type)
    cheats = rt.find_cheats()
    answer = [c for c in cheats if c.saving >= 100]
    print(f'Part 1: {len(answer)}')


@timer(TimeUnit.s)
def part2(input_type: InputType):
    rt = parse(input_type)
    cheats = rt.find_cheats(cheat_time=20)
    answer = [c for c in cheats.values() if c.saving >= 100]
    print(f'Part 2: {len(answer)}')


if __name__ == '__main__':
    #part1(input_type=InputType.INPUT)
    part2(input_type=InputType.INPUT)