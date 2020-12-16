import math
import sys
from collections import defaultdict
from typing import List, Tuple

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


class Rule:
    def __init__(self, rules_text: str):
        self.name = str()
        self.range_low = range(0)
        self.range_high = range(0)
        self._parse_text(text=rules_text)

    def _parse_text(self, text: str):
        name, ranges = text.split(":")
        self.name = name
        range_low, range_high = ranges.split(" or ")
        l1, l2 = [int(i) for i in range_low.split("-")]
        h1, h2 = [int(i) for i in range_high.split("-")]
        self.range_low = range(l1, l2+1)
        self.range_high = range(h1, h2+1)


def main(input_file: str) -> int:
    rules, your_ticket, nearby_tickets = parse_input(file=input_file)

    # Scanning error rate (part 1)
    error_rate = get_scanning_error_rate(rules=rules, tickets=nearby_tickets)
    print(f"Scanning error rate: {error_rate}\n")

    # Sort rules to match column values
    valid_tickets = [t for t in nearby_tickets if ticket_is_valid(rules=rules, ticket=t)]
    sort_rules(rules=rules, tickets=valid_tickets)

    # Product of departure fields (part 2)
    product = 1
    print(".------ Your ticket ------.")
    for i, rule in enumerate(rules):
        departure = rule.name.startswith("departure")
        print(f"| {'*' if departure else ' '} {rule.name}: {your_ticket[i]}")
        if departure:
            product = math.prod([product, your_ticket[i]])
    print("'-------------------------'")
    print(f"Product of all 'departure' fields: {product}")

    return 0


def parse_input(file: str) -> Tuple[List[Rule], List[int], List[List[int]]]:
    sections = []
    section = []
    for line in read_lines(file):
        if line == "":
            sections.append(section)
            section = []
            continue
        section.append(line)
    sections.append(section)

    rules = []
    for line in sections[0]:
        rules.append(Rule(rules_text=line))
    your_ticket = [int(i) for i in sections[1][1].split(",")]
    nearby_tickets = [[int(i) for i in t.split(",")] for t in sections[2][1:]]

    return rules, your_ticket, nearby_tickets


def find_invalid_values(rules: List[Rule], ticket: List[int]) -> List[int]:
    valid = []
    for value in ticket:
        for rule in rules:
            if value in rule.range_low or value in rule.range_high:
                valid.append(value)

    return [v for v in ticket if v not in valid]


def get_scanning_error_rate(rules: List[Rule], tickets: List[List[int]]) -> int:
    error_rate = 0
    for ticket in tickets:
        invalid = find_invalid_values(rules=rules, ticket=ticket)
        error_rate += sum(invalid)
    return error_rate


def ticket_is_valid(rules: List[Rule], ticket: List[int]) -> bool:
    if len(find_invalid_values(rules=rules, ticket=ticket)):
        return False
    return True


def sort_rules(rules: List[Rule], tickets: List[List[int]]):
    # Store all possible column values for each rule: {rule: [columns]}
    possible_columns = defaultdict(list)
    columns = [[t[i] for t in tickets] for i in range(len(tickets[0]))]
    for i, column in enumerate(columns):
        for rule in rules:
            valid = True
            for value in column:
                if value not in rule.range_low and value not in rule.range_high:
                    valid = False
                    break
            if valid is True:
                possible_columns[rule.name].append(i)

    # Pare down the list of possible columns by looking at single-column restraints.
    # If a field is only valid for a single column, remove that column from other rules' possibilities.
    while max([len(v) for v in possible_columns.values()]) > 1:
        constraints = []
        for rule, columns in possible_columns.items():
            if len(columns) == 1:
                constraints.append(columns[0])
        for rule, columns in list(possible_columns.items()):
            if len(columns) > 1:
                for c in constraints:
                    if c in columns:
                        possible_columns[rule].remove(c)

    # Sort the rules list now that there's just one possible column for each.
    rules.sort(key=lambda r: possible_columns[r.name])


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
