from typing import List


def union_lists(*lists: List):
    sets = [set(lst) for lst in lists]
    return list(sets[0].union(*sets[1:]))


def intersect_lists(*lists: List):
    sets = [set(lst) for lst in lists]
    return list(sets[0].intersection(*sets[1:]))
