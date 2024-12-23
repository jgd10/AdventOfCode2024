from aoc import parse_file, Point, timer, TimeUnit, InputType, Direction
from dataclasses import dataclass


NUMPAD_ROUTES = {
    'A9': '^^^A',
    '96': 'vA',
    '65': '<A',
    '5A': 'vv>A',
    'A1': '^<<A',
    '14': '^A',
    '43': 'v>>A',
    '3A': 'vA',
    'A5': '<^^A',
    '52': 'vA',
    '28': '^^A',
    '8A': 'vvv>A',
    'A6': '^^A',
    '67': '<<^A',
    '70': '>vvvA',
    '0A': '>A',
    '97': '<<A',
    '73': 'vv>>A',
    'A0': '<A',
    '02': '^A',
    '29': '^^>A',
    '9A': 'vvvA',
    '98': '<A',
    '80': 'vvvA',
    '17': '^^A',
    '79': '>>A',
    'A4': '^^<<A',
    '45': '>A',
    '56': '>A',
    '6A': 'vvA',
    'A3': '^A',
    '37': '<<^^A',
}

DPAD_ROUTES = {
    'Av': '<vA',
    'A>': 'vA',
    'A<': 'v<<A',
    'A^': '<A',
    '^^': 'A',
    'vv': 'A',
    '>>': 'A',
    '<<': 'A',
    'AA': 'A',
    '>v': '<A',
    '>A': '^A',
    '>^': '<^A',
    '><': '<<A',
    'v^': '^A',
    'v<': '<A',
    'v>': '>A',
    'vA': '^>A',
    '^A': '>A',
    '^>': 'v>A',
    '^v': 'vA',
    '^<': 'v<A',
    '<^': '>^A',
    '<v': '>A',
    '<>': '>>A',
    '<A': '>>^A',
}


@dataclass
class KeyPad:
    keys: dict[Point, str]
    _current_point: Point = None
    _points: dict[str, Point] = None
    is_robot: bool = True

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
        return cls(keys, is_robot=robot)

    def get_fastest_path(self, points: tuple[Point, Point]):
        route = self.keys[points[0]] + self.keys[points[1]]
        if self.is_robot:
            return DPAD_ROUTES[route]
        else:
            return NUMPAD_ROUTES[route]



@dataclass
class KeyPadStack:
    key_pads: list[KeyPad]

    def reset(self):
        for pad in self.key_pads:
            pad.current_point = pad.points['A']

    def get_commands_to_press(self, keys: str):
        key_pads = self.key_pads[:]
        while key_pads:
            current_pad = key_pads.pop()
            current_pad.current_point = current_pad.points['A']
            next_keys = []
            for cmd in keys:
                start = current_pad.current_point
                end = current_pad.points[cmd]
                pad_commands = current_pad.get_fastest_path((start, end))
                next_keys.append(pad_commands)
                current_pad.current_point = end
            keys = ''.join(next_keys)
        return keys


def get_move_counts_n_robots_above(stack: KeyPadStack):
    moves = {v for v in DPAD_ROUTES.values()}
    move_counts = {}
    for move in moves: # DPAD_ROUTES:
        stack.reset()
        commands = stack.get_commands_to_press(move)
        move_counts[move] = len(commands)
    return move_counts


@timer(TimeUnit.ms)
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
    print(f'Part 1: {total}')


@timer(TimeUnit.s)
def part2(input_type: InputType):
    key_presses = parse_file(input_type)
    robot_keypads = [KeyPad.from_text_file(robot=True) for _ in range(12)]
    robot_keypads2 = [KeyPad.from_text_file(robot=True) for _ in range(13)]
    door_keypad = KeyPad.from_text_file(robot=False)
    kps = KeyPadStack([*robot_keypads, door_keypad])
    total = 0
    move_counts = get_move_counts_n_robots_above(KeyPadStack(robot_keypads2))
    for code_press in key_presses:
        commands = kps.get_commands_to_press(code_press)
        num_commands = sum([move_counts[c+'A'] for c in
                           commands.split('A')]) - 1
        number = int(code_press.replace('A', ''))
        total += num_commands * number
    print(f'Part 2: {total}')


if __name__ == '__main__':
    part1(InputType.INPUT)
    part2(InputType.INPUT)