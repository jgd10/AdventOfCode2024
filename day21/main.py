from aoc import parse_file, Point, timer, TimeUnit, InputType, Direction
from dataclasses import dataclass
from itertools import permutations
import functools


@dataclass
class KeyPad:
    keys: dict[Point, str]
    _fastest_paths: dict[tuple[Point, Point], str] = None
    _fastest_paths_by_key: dict[tuple[str, str], str] = None
    _current_point: Point = None
    _points: dict[str, Point] = None

    def reset(self):
        self._current_point = self.points['A']

    @property
    def points(self):
        if self._points is None:
            self._points = {v: k for k, v in self.keys.items()}
        return self._points

    @property
    def current_point(self):
        if self._current_point is None:
            self._current_point = [p for p, v in self.keys.items()
                                   if v == 'A'][0]
        return self._current_point

    @current_point.setter
    def current_point(self, value: Point):
        self._current_point = value

    @classmethod
    def from_text_file(cls, robot: bool = True):
        if robot:
            filepath = 'keypad.txt'
        else:
            filepath = 'doorpad.txt'
        with open(filepath) as f:
            data = [s.strip('\n') for s in f.readlines()]
        keys = {}
        for j, row in enumerate(data):
            for i, c in enumerate(row):
                p = Point(i, j)
                if c == '.':
                    continue
                keys[p] = c
        return cls(keys)

    def get_fastest_path(self, points: tuple[Point, Point]):
        if points[0] == points[1]:
            return ''
        start, end = points
        diff = end.diff(start)
        if diff.x < 0:
            x_commands = '<'*abs(diff.x)
        elif diff.x > 0:
            x_commands = '>'*diff.x
        else:
            x_commands = ''
        if diff.y < 0:
            y_commands = '^'*abs(diff.y)
        elif diff.y > 0:
            y_commands = 'v'*diff.y
        else:
            y_commands = ''
        if Point(points[0].x + diff.x, points[0].y) not in self.keys:
            return y_commands + x_commands
        if Point(points[0].x, points[0].y + diff.y) not in self.keys:
            return x_commands + y_commands
        return x_commands + y_commands

    def is_valid_command(self, command: str, start, end) -> bool:
        point = start
        if command[-1] != 'A':
            return False
        for cmd in command:
            match cmd:
                case '>':
                    point = point.point_in_direction(Direction.E)
                case '^':
                    point = point.point_in_direction(Direction.N)
                case 'v':
                    point = point.point_in_direction(Direction.S)
                case '<':
                    point = point.point_in_direction(Direction.W)
                case 'A':
                    continue
                case _:
                    raise ValueError
            if point not in self.keys:
                return False
        if point != end:
            return False
        return True

    def optimise(self, upper_keypads: 'list[KeyPad]'):
        self.get_fastest_paths()
        new_fastest_paths = {}

        for points, commands in self.fastest_paths.items():
            optimal_commands = commands
            if len(set(commands)) != 2:
                new_fastest_paths[points] = optimal_commands
                continue
            shortest_command_length = 9999999
            for cmds in permutations(commands):
                string_command = ''.join(cmds) + 'A'
                if self.is_valid_command(string_command, *points):
                    top_command = self.get_upper_commands(
                        string_command, upper_keypads
                    )
                if len(top_command) < shortest_command_length:
                    shortest_command_length = len(top_command)
                    optimal_commands = ''.join(cmds)
            new_fastest_paths[points] = optimal_commands

        self._fastest_paths = new_fastest_paths
        self._fastest_paths_by_key = {(self.keys[p[0]], self.keys[p[
            0]]): path for p, path in self._fastest_paths.items()}

    @staticmethod
    def get_upper_commands(string_command, upper_keypads):
        next_keys = []
        upper_pads = upper_keypads[:]
        while upper_pads:
            upper_keypad = upper_pads.pop()
            for cmd in string_command:
                start = upper_keypad.current_point
                end = upper_keypad.points[cmd]
                pad_commands = upper_keypad.fastest_paths[(start, end)]
                next_keys.append(pad_commands + 'A')
                upper_keypad.current_point = end
            string_command = ''.join(next_keys)
        return string_command

    def get_fastest_paths(self):
        self._fastest_paths = {}
        for point1 in self.keys:
            for point2 in self.keys:
                points = (point1, point2)
                self._fastest_paths[points] = self.get_fastest_path(points)

    @property
    def fastest_paths(self):
        if self._fastest_paths is None:
            self._fastest_paths = {}
            self.get_fastest_paths()
            self._fastest_paths_by_key = {(self.keys[p[0]], self.keys[p[
                0]]): path for p, path in self._fastest_paths.items()}
        return self._fastest_paths

    @property
    def fastest_paths_by_key(self):
        if self._fastest_paths_by_key is None:
            self._fastest_paths = {}
            self.get_fastest_paths()
            self._fastest_paths_by_key = {(self.keys[p[0]], self.keys[p[
                0]]): path for p, path in self._fastest_paths.items()}
        return self._fastest_paths_by_key



@dataclass
class KeyPadStack:
    key_pads: list[KeyPad]

    def get_commands_to_press(self, keys: str):
        key_pads = self.key_pads[:]
        while key_pads:
            current_pad = key_pads.pop()
            current_pad.optimise(key_pads)
            current_pad.reset()
            for pad in key_pads:
                pad.reset()
            next_keys = []
            for cmd in keys:
                start = current_pad.current_point
                end = current_pad.points[cmd]
                pad_commands = current_pad.fastest_paths[(start, end)]
                next_keys.append(pad_commands+'A')
                current_pad.current_point = end
            keys = ''.join(next_keys)
        return keys


def part1(input_type: InputType):
    key_presses = parse_file(input_type)
    robot_keypads = [KeyPad.from_text_file(robot=True) for _ in range(2)]
    door_keypad = KeyPad.from_text_file(robot=False)
    kps = KeyPadStack([*robot_keypads, door_keypad])
    total = 0
    for code_press in key_presses:
        commands = kps.get_commands_to_press(code_press)
        number = int(code_press.replace('A', ''))
        total += len(commands) * number
        print(code_press, len(commands), number, commands)
    print(f'Part 1: {total}')


def part2(input_type: InputType):
    key_presses = parse_file(input_type)
    robot_keypads = [KeyPad.from_text_file(robot=True) for _ in range(25)]
    door_keypad = KeyPad.from_text_file(robot=False)
    kps = KeyPadStack([*robot_keypads, door_keypad])
    total = 0
    for code_press in key_presses:
        commands = kps.get_commands_to_press(code_press)
        number = int(code_press.replace('A', ''))
        total += len(commands) * number
        print(code_press, len(commands), number, commands)
    print(f'Part 2: {total}')


if __name__ == '__main__':
    part1(InputType.INPUT)
    part2(InputType.INPUT)