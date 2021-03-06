import math
import sys

from utils.input_file import file_path_from_args
from utils.math_utils import find_terms
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    number_list = [int(line) for line in read_lines(input_file) if is_int(line)]

    for term_count in (2, 3):
        terms = find_terms(terms=number_list, sum_=2020, term_count=term_count)
        if terms is not None:
            terms_str = " * ".join([str(t) for t in terms])
            print(f"{terms_str} = {math.prod(terms)}")
        else:
            print(f"No {term_count} terms found that sum to 2020.")

    return 0


def is_int(string: str) -> bool:
    """ Check whether a string can resolve to an integer. """
    if not isinstance(string, str):
        return False

    # noinspection PyBroadException
    try:
        int(string)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
