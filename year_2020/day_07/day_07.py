from __future__ import annotations

import re
import sys

from collections import namedtuple
from typing import List

from utils.input_file import file_path_from_args
from utils.print_fn import print
from utils.read_lines import read_lines


Contents = namedtuple("Rule", "num name")


name_re = re.compile(r"(?P<name>.+) bag(?:s)?", re.I)
contains_re = re.compile(r"(?P<num>[\d]+)\s(?P<name>.+?)\sbag(?:s)?", re.I)


class Bags:
    def __init__(self, input_file: str):
        self._bags = []

        self._parse_input_file(file=input_file)

    def _parse_input_file(self, file: str):
        for line in read_lines(file):
            self._bags.append(Bag(rule_text=line))

    @property
    def all_bags(self) -> List[Bag]:
        for bag in self._bags:
            yield bag

    def find(self, name: str) -> Bag or None:
        for bag in self.all_bags:
            if bag.name == name:
                return bag
        return None


BAGS = None


class Bag:
    def __init__(self, rule_text):
        self.name = None
        self.contains = []
        self._parse_text(text=rule_text)

    def _parse_text(self, text: str):
        name, contains = text.split(" contain ")
        self.name = name_re.match(name).group("name")

        if contains == "no other bags.":
            return
        else:
            matches = contains_re.finditer(contains)
            for match in matches:
                num = int(match.group("num"))
                name = match.group("name")
                self.contains.append(Contents(num, name))


def main(input_file: str) -> int:
    global BAGS
    BAGS = Bags(input_file=input_file)

    count = 0
    for bag in BAGS.all_bags:
        if can_contain(bag, "shiny gold"):
            count += 1

    print(f"{count} bags can contain a shiny gold bag.")

    children = count_children(BAGS.find("shiny gold"))
    print(f"Shiny gold bag can hold {children} other bags.")
    return 0


def can_contain(bag: Bag, name: str) -> bool:
    for contents in bag.contains:  # type: Contents
        if contents.name == name:
            return True
        elif can_contain(bag=BAGS.find(contents.name), name=name):
            return True
    return False


def count_children(bag: Bag) -> int:
    children = 0
    for contents in bag.contains:  # type: Contents
        children += (contents.num * (count_children(bag=BAGS.find(contents.name)) + 1))
    return children


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
