from itertools import combinations
from typing import List, Tuple


def find_terms(terms: List[int], sum_: int, term_count: int) -> Tuple[int, ...] or None:
    """ Find terms from a list that equal the sum. """
    for combination in combinations(terms, term_count):
        if sum(combination) == sum_:
            return combination
    return None
