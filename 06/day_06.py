import os
from typing import List


def main():
    input_file = os.path.join(os.path.dirname(__file__), "input.txt")

    groups = get_groups(input_file=input_file)

    union_count = 0
    for group in groups:
        union = union_lists(*group)
        union_count += len(union)

    intersection_count = 0
    for group in groups:
        intersection = intersect_lists(*group)
        intersection_count += len(intersection)

    print(f"Sum of all counts is {union_count} (Union)")
    print(f"Sum of all counts is {intersection_count} (Intersection)")


def get_groups(input_file: str) -> List[List]:
    with open(input_file, 'r') as fp:
        lines = [line.strip() for line in fp.readlines()]

    return split_list(lst=lines, separator="")


def split_list(lst: list, separator: str) -> List[List]:
    """ Split list into sub-lists based on a separator (like str.split). """
    grouped_list = []
    remainder = lst
    while len(remainder):
        if separator in remainder:
            split_index = remainder.index(separator)
            grouped_list.append(remainder[:split_index])
            remainder = remainder[split_index+1:]
        else:
            grouped_list.append(remainder)
            remainder = []
    return grouped_list


def union_lists(*lists: List):
    sets = [set(lst) for lst in lists]
    return list(sets[0].union(*sets[1:]))


def intersect_lists(*lists: List):
    sets = [set(lst) for lst in lists]
    return list(sets[0].intersection(*sets[1:]))


if __name__ == "__main__":
    main()
