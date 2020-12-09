import sys

from utils.input_file import file_path_from_args
from utils.program import Instruction, Program


def main(input_file: str) -> int:
    prog = Program.from_file(file=input_file)

    try:
        prog.run()
    except RecursionError as e:
        print(f"RecursionError: {e}")
        print(f"Accumulator: {prog.accumulator}")
        repair_program(prog)
        print(f"Accumulator: {prog.accumulator}")
    return 0


def repair_program(program: Program):
    print(f"Repairing...")

    original_instructions = program.instructions
    for address in program.visited_addresses:
        instruction = program.instructions[address]  # type: Instruction
        if instruction.operation in ["nop", "jmp"]:
            old_instruction = str(instruction)
            new_operation = "nop" if instruction.operation == "jmp" else "jmp"
            program.modify_instruction(address=address, operation=new_operation)
            print(f"Modified instruction @{address}: [{old_instruction}] -> [{instruction}]")
            try:
                program.run()
                print(f"Modification successful!")
                break
            except RecursionError as e:
                print(f"Modification failed: {e}")
                program.instructions = original_instructions


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
