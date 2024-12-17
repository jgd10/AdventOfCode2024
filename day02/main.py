def get_data():
    with open('./input.txt') as f:
        data = [s.strip('\n') for s in f.readlines()]
    return data


def part1():    
    data = get_data()
    counter = 0
    for row in data:
        safe = True
        line = [int(n) for n in row.split()]
        diffs = []

        prev = line.pop(0)
        for n in line:
            diffs.append(n-prev)
            prev = n
        if all([n < 0 for n in diffs]) or all([n > 0 for n in diffs]):
            pass
        else:
            safe = False
        unique_diffs = {abs(n) for n in diffs}
        allowed_diffs = {1, 2, 3}
        if unique_diffs.issubset(allowed_diffs):
            pass
        else:
            safe = False
        if safe:
            counter += 1
    print(f'Part 1: {counter}')


def get_diffs(line):
    diffs = []
    prev = line.pop(0)
    for n in line:
        diffs.append(n-prev)
        prev = n
    return diffs

def check_diffs(diffs):
    safe = True
    if all([n < 0 for n in diffs]) or all([n > 0 for n in diffs]):
        pass
    else:
        safe = False
    unique_diffs = {abs(n) for n in diffs}
    allowed_diffs = {1, 2, 3}
    if unique_diffs.issubset(allowed_diffs):
        pass
    else:
        safe = False
    return safe

def part2():    
    data = get_data()
    counter = 0
    for row in data:
        line = [int(n) for n in row.split()]
        diffs = get_diffs(line[:])
        safe = check_diffs(diffs)
        if not safe:
            safe = check_tolerance(line[:])
        if safe:
            #print(line)
            counter += 1
    print(f'Part 2: {counter}')


def check_tolerance(nums):
    for j, _ in enumerate(nums):
        new = nums[:]
        new.pop(j)
        diffs = get_diffs(new[:])
        safe = check_diffs(diffs[:])
        if safe:
            return True
    return False


if __name__ == '__main__':
    part1()
    part2()
