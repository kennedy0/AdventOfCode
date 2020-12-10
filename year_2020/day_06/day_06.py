import sys
from typing import List

from utils.input_file import file_path_from_args
from utils.lists import intersect_lists, union_lists
from utils.print_fn import print
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    groups = split_list(lst=list(read_lines(input_file)), separator="")

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
    return 0


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


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
