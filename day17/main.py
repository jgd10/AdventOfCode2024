from aoc import parse_file, InputType, timer, TimeUnit
from dataclasses import dataclass


@dataclass
class Program:
    a: int
    b: int
    c: int
    program: list[int]
    instruction_pointer: int = 0
    result: list[int] = None

    def run(self):
        self.instruction_pointer = 0
        while self.ip < len(self.program):
            opcode = self.program[self.ip]
            operand = self.program[self.ip + 1]
            self.do_instruction(opcode, operand)
        return ','.join([str(i) for i in self.result])

    def output(self, value: int):
        if self.result is None:
            self.result = [value]
        else:
            self.result.append(value)

    @property
    def ip(self):
        return self.instruction_pointer

    def get_operand(self, number: int, literal: bool = True) -> int:
        if literal:
            return number
        match number:
            case 0 |1 | 2 | 3:
                return number
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise NotImplementedError
            case _:
                raise ValueError

    def reset(self, a: int):
        self.result = []
        self.a = a

    @staticmethod
    def calculate_a(coefficients: list[int]) -> int:
        return sum([c * 8 ** i for i, c in enumerate(coefficients)])

    def find_optimal_a(self):
        coefficients = [0 for _ in self.program] + [0]
        coefficient_index: int = 0
        a = 0
        self.run()
        reversed_program = [j for j in reversed(self.program)]
        reversed_result = [k for k in reversed(self.result)]
        while self.program != self.result:
            i = 0
            while reversed_program[:coefficient_index] != reversed_result[:coefficient_index]:
                coefficients[coefficient_index] = i
                a = self.calculate_a([i for i in reversed(coefficients)])
                self.reset(a=a)
                self.run()
                i += 1
                reversed_result = [k for k in reversed(self.result)]
            coefficient_index += 1
        return a

    def do_instruction(self, opcode: int, number: int):
        match opcode:
            case 0:  # adv
                operand = self.get_operand(number, literal=False)
                self.a = self.a // (2**operand)
                self.instruction_pointer += 2
            case 1:  # bxl
                operand = self.get_operand(number, literal=True)
                self.b ^= operand
                self.instruction_pointer += 2
            case 2:  # bst
                operand = self.get_operand(number, literal=False)
                self.b = operand % 8
                self.instruction_pointer += 2
            case 3:  # jnz
                operand = self.get_operand(number, literal=True)
                if self.a != 0:
                    self.instruction_pointer = operand
                else:
                    self.instruction_pointer += 2
            case 4:  # bxc
                self.b ^= self.c
                self.instruction_pointer += 2
            case 5:  # out
                operand = self.get_operand(number, literal=False)
                self.output(operand % 8)
                self.instruction_pointer += 2
            case 6:  # bdv
                operand = self.get_operand(number, literal=False)
                self.b = self.a // (2 ** operand)
                self.instruction_pointer += 2
            case 7:
                operand = self.get_operand(number, literal=False)
                self.c = self.a // (2 ** operand)
                self.instruction_pointer += 2


def parse(input_type: InputType):
    data = parse_file(input_type)
    a, b, c = None, None, None
    program = []
    for row in data:
        if 'register a' in row.lower():
            a = int(row.lower().replace('register a: ', ''))
        if 'register b' in row.lower():
            b = int(row.lower().replace('register b: ', ''))
        if 'register c' in row.lower():
            c = int(row.lower().replace('register c: ', ''))
        if 'program' in row.lower():
            program = [int(v) for v in row.lower().replace('program: ', '').split(',')]
    return Program(a, b, c, program)


@timer(unit=TimeUnit.ms)
def part1(input_type: InputType):
    program = parse(input_type)
    print(f'Part 1: {program.run()}')


@timer(unit=TimeUnit.ms)
def part2(input_type: InputType):
    program = parse(input_type)
    print(f'Part 2: {program.find_optimal_a()}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    part1(InputType.INPUT)
    part2(InputType.INPUT)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
