from __future__ import annotations
import sys
from collections import defaultdict

from utils.input_file import file_path_from_args
from utils.memoize import memoize
from utils.read_lines import read_lines
from utils.timer import Timer

ADAPTERS = [0]


def main(input_file: str) -> int:
    global ADAPTERS
    ADAPTERS += sorted([int(line) for line in read_lines(input_file)])
    ADAPTERS.append(max(ADAPTERS) + 3)  # Built-in adapter

    find_differences()

    with Timer():
        combinations = find_combinations()
    print(f"Total adapter arrangements:  {combinations}")

    return 0


def find_differences():
    totals = defaultdict(lambda: 0)

    current_joltage = 0
    for joltage in ADAPTERS:
        difference = joltage - current_joltage
        totals[difference] += 1
        current_joltage = joltage

    print(f"1-jolt differences: {totals[1]}")
    print(f"3-jolt differences: {totals[3]}")
    print(f"{totals[1]} * {totals[3]} = {totals[1]*totals[3]}")


@memoize
def find_combinations(list_position: int = 0, num_combinations: int = 0):
    if list_position == len(ADAPTERS) - 1:
        return num_combinations + 1

    combinations = 0
    valid_joltages = [j for j in ADAPTERS[list_position+1:list_position+4] if 1 <= j-ADAPTERS[list_position] <= 3]
    for jolt in valid_joltages:
        combinations += find_combinations(list_position=ADAPTERS.index(jolt), num_combinations=num_combinations)

    return combinations


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
