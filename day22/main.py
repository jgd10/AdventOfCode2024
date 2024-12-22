from aoc import parse_file, InputType, timer, TimeUnit
from dataclasses import dataclass
import csv


def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@dataclass
class MarketHistory:
    prices: list[list[int]]
    _changes: list[list[int]] = None
    _sequence_vals: dict[tuple[int, tuple[int, ...]], int] = None

    def find_sequence_values(self):
        for j, changes in enumerate(self.changes):
            n = len(changes)
            for i in range(n):
                seq = tuple(changes[i:i+4])
                if len(seq) != 4:
                    continue
                if (j, seq) in self.sequence_vals:
                    pass
                else:
                    self.sequence_vals[(j, seq)] = self.prices[j][i+4]
        return self.sequence_vals

    def find_max_available_bananas(self):
        max_bananas = 0
        n = len(self.changes)
        all_seqs = {k[1] for k in self.sequence_vals.keys()}
        for seq in all_seqs:
            total = 0
            for i in range(n):
                if (i, seq) in self.sequence_vals:
                    total += self.sequence_vals[(i, seq)]
            max_bananas = max(total, max_bananas)
        return max_bananas

    @property
    def sequence_vals(self):
        if self._sequence_vals is None:
            self._sequence_vals = {}
        return self._sequence_vals

    @classmethod
    def from_file(cls, input_type: InputType):
        with open(f'prices_{input_type}.csv') as f:
            reader = csv.reader(f, delimiter=',')
            data = [[int(s) for s in row] for row in reader]
        return cls(data)

    @property
    def changes(self):
        if self._changes is None:
            self._changes = []
            self.find_changes()
        return self._changes

    def find_changes(self):
        changes = []
        for prices in self.prices:
            previous = None
            change = []
            for price in prices:
                if previous is None:
                    previous = price
                    continue
                change.append(price-previous)
                previous = price
            changes.append(change)
        self._changes = changes


@dataclass
class MonkeyMarket:
    secrets: list[int]
    _prices: list[list[int]] = None

    def numbers_after(self, counter: int):
        for i in range(counter):
            self.next()
        return self.secrets

    @property
    def prices(self):
        if self._prices is None:
            self._prices = [[int(str(s)[-1])] for s in self.secrets]
        return self._prices

    def save_prices(self, input_type: InputType):
        with open(f'prices_{input_type}.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.prices)

    def next(self):
        new = []
        for secret in self.secrets:
            value = secret * 64
            value = secret ^ value
            new_ = value % 16777216
            value = new_ // 32
            value ^= new_
            new_ = value % 16777216
            value *= 2048
            value = value ^ new_
            value = value % 16777216
            new.append(value)
        for secret, prices in zip(new, self.prices):
            string = str(secret)
            price = int(string[-1])
            prices.append(price)
        self.secrets = new



@timer(TimeUnit.s)
def part1(input_type: InputType):
    data = parse_file(input_type)
    secrets = [int(row) for row in data]
    market = MonkeyMarket(secrets)
    secrets = market.numbers_after(2000)
    print(f'Part 1: {sum(secrets)}')


@timer(TimeUnit.s)
def part2(input_type: InputType):
    #data = parse_file(input_type)
    #secrets = [int(row) for row in data]
    #market = MonkeyMarket(secrets)
    #secrets = market.numbers_after(2000)
    #market.save_prices(input_type)
    mh = MarketHistory.from_file(input_type)
    sequences = mh.find_sequence_values()
    print(f'Part 2: {mh.find_max_available_bananas()}')


if __name__ == '__main__':
    #part1(InputType.INPUT)
    part2(InputType.INPUT)

