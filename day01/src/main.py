
def get_input_data():
    with open('../input.txt') as f:
        lines = [s.strip('\n') for s in f.readlines()]
    lefties = []
    righties = []

    for line in lines:
        left, right = line.split()
        lefties.append(int(left))
        righties.append(int(right))
    return lefties, righties


def part1():
    lefties, righties = get_input_data()
    lefties.sort()
    righties.sort()
    total = 0

    for lhs, rhs in zip(lefties, righties):
        total += abs(lhs - rhs)

    print(f'Part 1 {total}')


def part2():
    lefties, righties = get_input_data()
    total = 0
    for num in lefties:
        total += num * righties.count(num)
    print(f'Part 2 {total}')


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
