import sys
from collections import defaultdict
from typing import List

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    starting_numbers = [int(n) for n in list(read_lines(input_file))[0].split(",")]

    print("Starting numbers:", starting_numbers)
    memory_game(starting_numbers=starting_numbers, rounds=2020)
    memory_game(starting_numbers=starting_numbers, rounds=30000000)
    return 0


def memory_game(starting_numbers: List[int], rounds: int):
    # History dict stores: {number: last round spoken}
    history = defaultdict(int)

    # Init history with the first n-1 numbers
    for i, number in enumerate(starting_numbers[:-1], start=1):
        history[number] = i

    n = starting_numbers[-1]  # n is last number spoken
    for i in range(len(starting_numbers), rounds):
        round_last_spoken = history[n]
        history[n] = i
        if round_last_spoken == 0:
            n = 0
        else:
            n = i - round_last_spoken

    print(f"Number spoken on round {rounds}: {n}")


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
