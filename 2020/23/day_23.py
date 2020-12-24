from __future__ import annotations
import math
import sys
from typing import Dict, List

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    # Part 1
    cup_list = get_cup_list(file=input_file)
    cups = build_cups_dict(cup_list=cup_list)
    mix_cups(cups=cups, current=cup_list[0], num_rounds=100)

    cup = cups[1]
    cup_str = ""
    while cup != 1:
        cup_str += str(cup)
        cup = cups[cup]
    print(f"Labels after cup 1: {cup_str}")

    # Part 2
    cup_list = get_cup_list(file=input_file, extra_cups=1000000)
    cups = build_cups_dict(cup_list=cup_list)
    mix_cups(cups=cups, current=cup_list[0], num_rounds=10000000)

    cup_a = cups[1]
    cup_b = cups[cup_a]
    print(f"{cup_a} * {cup_b} = {cup_a * cup_b}")
    return 0


def parse_input(file: str) -> List:
    lines = list(read_lines(file))
    return [int(c) for c in lines[0]]


def get_cup_list(file: str, extra_cups: int = None) -> List[int]:
    cup_list = parse_input(file=file)
    if extra_cups is not None:
        cup_list += list(range(extra_cups+1))[10:]
    return cup_list


def build_cups_dict(cup_list: List[int]) -> Dict:
    """ Build a faux linked-list with a dictionary. """
    cups = dict()
    for i, cup in enumerate(cup_list):
        if i == len(cup_list) - 1:
            cups.update({cup: cup_list[0]})
        else:
            cups.update({cup: cup_list[i+1]})
    return cups


def do_move(cups: dict, current: int, max_value: int):
    destination = current - 1

    pick_up_start = cups[current]
    pick_up_end = cups[cups[cups[current]]]
    cups[current] = cups[pick_up_end]

    while destination in [pick_up_start, cups[pick_up_start], pick_up_end] or destination < 1:
        destination -= 1
        if destination < 1:
            destination = max_value

    cups[pick_up_end] = cups[destination]
    cups[destination] = pick_up_start


def mix_cups(cups: Dict, current: int, num_rounds: int):
    max_value = max(cups.keys())
    for x in range(num_rounds):
        do_move(cups=cups, current=current, max_value=max_value)
        current = cups[current]


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
