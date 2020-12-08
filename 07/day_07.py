import os
import re

from collections import namedtuple
from typing import List


Contents = namedtuple("Rule", "num name")


name_re = re.compile(r"(?P<name>.+) bag(?:s)?", re.I)
contains_re = re.compile(r"(?P<num>[\d]+)\s(?P<name>.+?)\sbag(?:s)?", re.I)


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


def get_bags(input_file: str) -> List[Bag]:
    bags = []
    with open(input_file, 'r') as fp:
        for line in fp.readlines():
            bags.append(Bag(rule_text=line.strip()))
    return bags


BAGS = get_bags(input_file=os.path.join(os.path.dirname(__file__), "input.txt"))


def main():
    count = 0
    for bag in BAGS:
        if can_contain(bag, "shiny gold"):
            count += 1

    print(f"{count} bags can contain a shiny gold bag.")

    children = count_children(find_bag("shiny gold"))
    print(f"Shiny gold bag can hold {children} other bags.")


def find_bag(name: str) -> Bag or None:
    for bag in BAGS:
        if bag.name == name:
            return bag
    return None


def can_contain(bag: Bag, name: str) -> bool:
    for contents in bag.contains:  # type: Contents
        if contents.name == name:
            return True
        elif can_contain(bag=find_bag(contents.name), name=name):
            return True
    return False


def count_children(bag: Bag) -> int:
    children = 0
    for contents in bag.contains:  # type: Contents
        children += (contents.num * (count_children(bag=find_bag(contents.name)) + 1))
    return children


if __name__ == "__main__":
    main()
