import math
import os

from itertools import combinations
from typing import List, Tuple


def main(term_count: int):
    input_file = os.path.join(os.path.dirname(__file__), "input.txt")
    number_list = get_number_list(input_file)

    if term_count < 2:
        raise RuntimeError("Term count must be at least 2.")
    elif term_count > len(number_list):
        raise RuntimeError("Term count is greater than input list.")

    terms = find_terms(terms=number_list, sum_=2020, term_count=term_count)
    if terms is not None:
        terms_str = " * ".join([str(t) for t in terms])
        print(f"{terms_str} = {math.prod(terms)}")
    else:
        print(f"No {term_count} terms found that sum to 2020.")


def get_number_list(file_path: str) -> List[int]:
    """ Return a list of integers from an input file. """
    with open(file_path, 'r') as fp:
        numbers = [line.strip() for line in fp.readlines()]
    number_list = [int(n) for n in numbers if is_int(n)]
    return number_list


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


def find_terms(terms: List[int], sum_: int, term_count: int) -> Tuple[int, ...] or None:
    """ Find terms from a list that equal the sum. """
    for combination in combinations(terms, term_count):
        if sum(combination) == sum_:
            return combination
    return None


if __name__ == "__main__":
    main(term_count=2)
    main(term_count=3)
