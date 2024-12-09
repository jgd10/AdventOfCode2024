
def get_last(a):
  for i, e in enumerate(reversed(a)):
    if e is not None:
      return len(a) - i - 1
  return -1

def parse() -> list[int | None]:
    with open('../input.txt') as f:
        data = [s.strip('\n') for s in f.readlines()]
        data = ''.join(data)

    counter = 0
    disk = []
    for i, character in enumerate(data):
        if i%2 == 0:
            block = [counter]*int(character)
            counter += 1
        else:
            block = [None]*int(character)
        disk.append(block)
    return [item for block in disk for item in block]


def parse2() -> list[list[int | None]]:
    with open('../input.txt') as f:
        data = [s.strip('\n') for s in f.readlines()]
        data = ''.join(data)

    counter = 0
    disk = []
    for i, character in enumerate(data):
        if i%2 == 0:
            block = [counter]*int(character)
            counter += 1
        else:
            block = [None]*int(character)
        if len(block) != 0:
            disk.append(block)
    return disk


def shuffle_blocks2(disk):
    while None in disk:
        first_none = disk.index(None)
        disk[first_none] = disk.pop(get_last(disk))
    return disk


def shuffle_blocks(disk: list[list[int | None]]) -> tuple[list[list[int]], bool]:
    empty_block_lengths = []
    filled_block_lengths = []
    for i, block in enumerate(disk):
        check_block = [b is None for b in block]
        if any(check_block):
            empty_block_lengths.append((len(block), i))
        else:
            filled_block_lengths.append((len(block), i))

    for empty_length, j in empty_block_lengths:
        for filled_block, i in reversed(filled_block_lengths):
            if empty_length >= filled_block and i > j:
                disk[i][:filled_block], disk[j]  = disk[j][:filled_block], disk[i][:filled_block]
                if empty_length != filled_block:
                    disk.insert(j+1, [None]*(empty_length-filled_block))
                return disk, False
    return disk, True


def part1():
    disk = parse()
    disk = shuffle_blocks2(disk)
    answer = sum([num*i for i, num in enumerate(disk)])
    print('Part 1:', answer)


def part2():
    disk = parse2()
    success = False
    while not success:
        disk, success = shuffle_blocks(disk)
    disk_nums = [i if i is not None else 0 for block in disk for i in block]
    answer = sum([num*i for i, num in enumerate(disk_nums)])
    print('Part 2:', answer)


if __name__ == '__main__':
    # part1()
    part2()
