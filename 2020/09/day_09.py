import sys
from typing import List

from utils.input_file import file_path_from_args
from utils.math_utils import find_terms
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    data = list(int(line) for line in read_lines(input_file))
    invalid = find_invalid(data=data, preamble=25)
    print(f"{invalid} is invalid.")

    weakness = find_encryption_weakness(data=data, value=invalid)
    print(f"encryption weakness is {weakness}")
    return 0


def find_invalid(data: List[int], preamble: int) -> int:
    for i, number in enumerate(data[preamble:], start=preamble):
        previous = data[i-preamble:i]
        terms = find_terms(terms=previous, sum_=number, term_count=2)
        if terms is None:
            return number


def find_encryption_weakness(data: List[int], value: int) -> int:
    term_count = 2
    while True:
        for i in range(len(data)-term_count+1):
            subset = data[i:i+term_count]
            if sum(subset) == value:
                return min(subset) + max(subset)
        term_count += 1


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
