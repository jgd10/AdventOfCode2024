from typing import Tuple


def scalar_digit_multiply(number: list[int], digit: int):
    result = []
    carry = 0
    for n in reversed(number):
        ans = str(n * digit + carry)
        if len(ans) > 1:
            carry = int(ans[:-1])
            ans = ans[-1]
        else:
            carry = 0
        result.insert(0, int(ans))
    if carry > 0:
        result.insert(0, carry)
    return result


def long_sum(data: list[list[int]]) -> tuple[int]:
    carry = 0
    result = []
    while any([len(row) > 0 for row in data]):
        total = sum([row.pop() for row in data if len(row) > 0])
        ans = str(total + carry)
        if len(ans) > 1:
            carry = int(ans[:-1])
            ans = ans[-1]
        else:
            carry = 0
        result.insert(0, int(ans))
    if carry > 0:
        result.insert(0, carry)
    return tuple(result)


def long_multiply(num1: tuple[int, ...], num2: tuple[int, ...]) -> tuple[int]:
    """Long multiplication.

    Equivalent to,

        num1
    x   num2
    --------
    ........
    --------

    :param num1:
    :param num2:
    :return:
    """
    results = []
    for i, n in enumerate(reversed(num2)):
        result = scalar_digit_multiply(num1, n)
        result.extend([0 for _ in range(i)])
        results.append(result)

    return long_sum(results)


def strip_leading_zeroes(number: tuple[int, ...]) -> tuple[int, ...]:
    new_num = []
    first_digit_reached = False
    for n in number:
        if n == 0 and first_digit_reached is not True:
            continue
        else:
            new_num.append(n)
            first_digit_reached = True
    if len(new_num) == 0:
        new_num = [0]
    return tuple(new_num)


def part1():
    """
    rules:

    - if 0 then becomes 1
    - if even number digits -> split in half (disregard leading 0)
    - otherwise * 2024
    """
    with open('../input.txt') as f:
        data = [s.strip('\n') for s in f.readlines()]
        data = data[0]
        nums = data.split(' ')
    numbers = [[int(c) for c in number] for number in nums]
    print(numbers)
    blinks = 25
    for i in range(blinks):
        print(i, len(numbers))
        new_numbers = []
        for number in numbers:
            if len(number) == 1 and number[0] == 0:
                new_numbers.append([1])
                continue
            if (length := len(number)) % 2 == 0:
                new_length = length // 2
                new_num1 = number[:new_length]
                new_num2 = strip_leading_zeroes(number[new_length:])
                new_numbers.append(new_num1)
                new_numbers.append(new_num2)
                continue
            new_numbers.append(long_multiply(number, [2, 0, 2, 4]))
        numbers = new_numbers[:]
    print(f'Part 1: {len(numbers)}')


def find_number_of_stones_after(blinks: int) -> int:
    with open('../input.txt') as f:
        data = [s.strip('\n') for s in f.readlines()]
        data = data[0]
        nums = data.split(' ')
    numbers = {tuple(int(c) for c in number) for number in nums}
    old_number_counts = {n: 1 for n in numbers}
    for i in range(blinks):
        new_counts = {}
        for number in old_number_counts:
            if len(number) == 1 and number[0] == 0:
                if (1,) not in new_counts:
                    new_counts[(1,)] = 0
                new_counts[(1,)] += old_number_counts[(0,)]
                continue
            if (length := len(number)) % 2 == 0:
                new_length = length // 2
                new_num1 = number[:new_length]
                new_num2 = strip_leading_zeroes(number[new_length:])
                if new_num1 not in new_counts:
                    new_counts[new_num1] = 0
                if new_num2 not in new_counts:
                    new_counts[new_num2] = 0
                new_counts[new_num1] += old_number_counts[number]
                new_counts[new_num2] += old_number_counts[number]
                continue
            new_num = long_multiply(number, (2, 0, 2, 4))
            if new_num not in new_counts:
                new_counts[new_num] = 0
            new_counts[new_num] += old_number_counts[number]
        old_number_counts = new_counts.copy()
    return sum([v for v in old_number_counts.values()])


def test():
    print(long_multiply((2, 0, 2, 4), (7,)))
    print(long_multiply((7,), (2, 0, 2, 4)))
    print(long_multiply((2,), (9, 9, 9, 9)))
    print(long_multiply((7,7,0,8), (2, 0, 2, 4)))
    print(strip_leading_zeroes((0,0,4)))
    print(strip_leading_zeroes((0, 0, 0)))
    print(strip_leading_zeroes((0, 0, 4, 1)))
    print(strip_leading_zeroes((0, 0, 4, 0, 0)))


def main():
    print(f'Part 1: {find_number_of_stones_after(25)}')
    print(f'Part 2: {find_number_of_stones_after(75)}')


if __name__ == '__main__':
    main()
