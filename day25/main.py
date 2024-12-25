from aoc import InputType, parse_file, timer, TimeUnit
from dataclasses import dataclass


@dataclass(frozen=True)
class Lock:
    pins: tuple[int, ...]

    def fits_key(self, key: 'Key'):
        return all([(p+t)<=5 for p,t in zip(self.pins, key.teeth)])

    @classmethod
    def from_rows(cls, rows):
        cols = [-1, -1, -1, -1, -1]
        for row in rows:
            for i, p in enumerate(row):
                if p == '#':
                    cols[i] += 1
        return cls(tuple(cols))


@dataclass(frozen=True)
class Key:
    teeth: tuple[int, ...]

    def fits_lock(self, lock: Lock):
        return all([(p+t)<=5 for p,t in zip(lock.pins, self.teeth)])


    @classmethod
    def from_rows(cls, rows):
        cols = [-1, -1, -1, -1, -1]
        for row in rows:
            for i, p in enumerate(row):
                if p == '#':
                    cols[i] += 1
        return cls(tuple(cols))


def parse(input_type: InputType):
    data = parse_file(input_type)
    lock_or_key = []
    locks = set()
    keys = set()
    for row in data:
        if not row:
            if all([c == '#' for c in lock_or_key[0]]):
                locks.add(Lock.from_rows(lock_or_key))
            else:
                keys.add(Key.from_rows(lock_or_key))
            lock_or_key = []
            continue
        lock_or_key.append(row)
    if lock_or_key:
        if all([c == '#' for c in lock_or_key[0]]):
            locks.add(Lock.from_rows(lock_or_key))
        else:
            keys.add(Key.from_rows(lock_or_key))
    return locks, keys


@timer(TimeUnit.ms)
def part1(input_type: InputType):
    locks, keys = parse(input_type)

    pairs = {(lock, key) for lock in locks
             for key in keys
             if lock.fits_key(key)}
    print(f'Part 1: {len(pairs)}')


if __name__ == '__main__':
    part1(InputType.INPUT)