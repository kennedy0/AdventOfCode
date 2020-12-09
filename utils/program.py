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
        self.address = 0
        self.accumulator = 0
        self.instructions = []
        self.history = []

    @classmethod
    def from_file(cls, file: str) -> Program:
        prog = Program()
        prog.load_instructions(file=file)
        return prog

    def load_instructions(self, file: str):
        self.instructions = []
        for line in read_lines(file):
            self.instructions.append(Instruction.from_text(text=line))

    def reset(self):
        self.address = 0
        self.accumulator = 0
        self.history = []

    def step(self):
        return

    def run(self):
        self.reset()

        while address < len(self.instructions):
            instruction = self.get_instruction(address)
            op = self.operation_dispatch[instruction.operation]
            offset = op(argument=instruction.argument)
            address += offset

        print(f"Program terminated. Accumulator is {self.accumulator}")
