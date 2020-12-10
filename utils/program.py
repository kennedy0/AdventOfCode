from __future__ import annotations

from utils.read_lines import read_lines


class Instruction:
    def __init__(self, operation: str = "nop", argument: int = 0):
        self.operation = operation
        self.argument = argument

    def __str__(self):
        return f"{self.operation} {self.argument:+d}"

    @classmethod
    def from_text(cls, text: str) -> Instruction:
        operation, argument = text.split(" ")
        return Instruction(operation=operation, argument=int(argument))


class Program:
    def __init__(self):

        self.address = 1
        self.accumulator = 0
        self.instructions = []
        self.visited_addresses = []

        self.operation_dispatch = {
            'acc': self.acc,
            'jmp': self.jmp,
            'nop': self.nop,
        }

    def acc(self, argument: int) -> int:
        self.accumulator += argument
        return 1

    def jmp(self, argument: int) -> int:
        return argument

    def nop(self, argument: int) -> int:
        return 1

    @classmethod
    def from_file(cls, file: str) -> Program:
        p = Program()
        p.load_instructions(file=file)
        return p

    def load_instructions(self, file: str):
        self.instructions = []
        for i, line in enumerate(read_lines(file), start=1):
            self.instructions.append(Instruction.from_text(text=line))

    def reset(self):
        self.address = 1
        self.accumulator = 0
        self.visited_addresses = []

    def get_instruction(self) -> Instruction:
        if self.address in self.visited_addresses:
            raise RecursionError(f"Address {self.address} has been visited already.")
        else:
            self.visited_addresses.insert(0, self.address)
            return self.instructions[self.address]

    def modify_instruction(self, address: int, operation: str = None, argument: str = None):
        if operation is not None:
            self.instructions[address].operation = operation
        if argument is not None:
            self.instructions[address].argument = argument

    def step(self):
        instruction = self.get_instruction()
        op = self.operation_dispatch[instruction.operation]
        result = op(argument=instruction.argument)  # noqa
        self.address += result

    def run(self):
        self.reset()
        while self.address < len(self.instructions):
            self.step()
