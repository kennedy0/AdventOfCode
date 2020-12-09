import sys

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


class Instruction:
    def __init__(self, instruction_text: str):
        self._operation = None
        self._argument = None
        self.parse_instruction_text(instruction_text)

    def parse_instruction_text(self, text: str):
        operation, argument = text.split(" ")
        self._operation = operation
        self._argument = int(argument)

    def __str__(self):
        return f"{self.operation} {self.argument:+d}"

    @property
    def operation(self) -> str:
        return self._operation

    @operation.setter
    def operation(self, value: str):
        self._operation = value

    @property
    def argument(self) -> int:
        return self._argument

    @argument.setter
    def argument(self, value: int):
        self._argument = int(value)


class Program:
    def __init__(self, instruction_file: str):
        self.accumulator = 0
        self.instructions = []
        self._original_instructions = []
        self.address_history = []

        self.operation_dispatch = {
            'acc': self.acc,
            'jmp': self.jmp,
            'nop': self.nop,
        }

        self.parse_instructions(instruction_file)

    def parse_instructions(self, file: str):
        for line in read_lines(file):
            self.instructions.append(Instruction(line))
        self._original_instructions = self.instructions

    def reset_instructions(self):
        self.instructions = self._original_instructions

    def modify_instruction(self, address: int, operation: str = None, argument: str = None):
        if operation is not None:
            self.instructions[address].operation = operation
        if argument is not None:
            self.instructions[address].argument = argument

    def acc(self, argument: int) -> int:
        self.accumulator += argument
        return 1

    def jmp(self, argument: int) -> int:
        return argument

    def nop(self, argument: int) -> int:
        return 1

    def get_instruction(self, address: int) -> Instruction:
        if address in self.address_history:
            raise RecursionError(f"Address {address} has been visited already. Accumulator is {self.accumulator}.")
        else:
            self.address_history.insert(0, address)
            return self.instructions[address]

    def run(self):
        address = 0
        self.accumulator = 0
        self.address_history = []

        while address < len(self.instructions):
            instruction = self.get_instruction(address)
            op = self.operation_dispatch[instruction.operation]
            offset = op(argument=instruction.argument)
            address += offset

        print(f"Program terminated. Accumulator is {self.accumulator}")


def main(input_file: str) -> int:
    prog = Program(instruction_file=input_file)
    try:
        prog.run()
    except RecursionError as e:
        print(f"RecursionError: {e}")
        print(f"Brute-forcing repair...\n")
        for address in prog.address_history:
            instruction = prog.instructions[address]  # type: Instruction
            if instruction.operation in ["nop", "jmp"]:
                old_instruction_str = str(instruction)
                new_operation = "nop" if instruction.operation == "jmp" else "jmp"
                prog.modify_instruction(address=address, operation=new_operation)
                print(f"Modified instruction @{address}: [{old_instruction_str}] -> [{instruction}]")
                try:
                    prog.run()
                    print(f"Modification successful!")
                    break
                except RecursionError as e:
                    print(f"Modification failed: {e}")
                    print("Resetting instructions...\n")
                    prog.reset_instructions()
    return 0


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
