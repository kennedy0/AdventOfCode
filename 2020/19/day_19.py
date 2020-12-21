import re
import sys
from typing import Any, AnyStr, Dict, List, Tuple

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


RULES = dict()
MESSAGES = list()


def main(input_file: str) -> int:
    parse_input(file=input_file)
    find_matches()

    print("Updating rules...")
    RULES.update({'8': "42 | 42 8"})
    RULES.update({'11': "42 31 | 42 11 31"})

    find_matches()
    return 0


def parse_input(file: str):
    lines = list(read_lines(file))
    index = lines.index("")

    for line in lines[:index]:
        key, value = line.split(":")
        RULES[key] = value.strip()

    for line in lines[index+1:]:
        MESSAGES.append(line)


def rule_to_re(rule: str) -> str:
    if rule in ["a", "b"]:
        return rule

    rule_str = ""

    rule_parts = [r.strip("\" ") for r in rule.split(" ")]
    for part in rule_parts:
        if part in ["a", "b", "|"]:
            rule_str += part
        elif part in ["8", "11"] and part in [r.strip("\" ") for r in RULES[part].split(" ")]:
            # part 2 loops
            if part == "8":
                part_sub = rule_to_re(rule='42')
                rule_str += f"(?:{part_sub})+"
            elif part == "11":
                part_sub_42 = rule_to_re(rule='42')
                rule_str_42 = f"(?:{part_sub_42})+"
                part_sub_31 = rule_to_re(rule='31')
                rule_str_31 = f"(?:{part_sub_31})+"
                rule_str += f"{rule_str_42}{rule_str_31}"
        else:
            part_sub = rule_to_re(rule=RULES[part])
            rule_str += f"(?:{part_sub})"

    return rule_str


def find_matches():
    rule_str = f"^{rule_to_re(rule=RULES['0'])}$"
    rule_zero_re = re.compile(rule_str)

    matches = []
    for message in MESSAGES:
        match = re.match(rule_zero_re, message)
        if match is not None:
            matches.append(match.group(0))

    print(f"Found {len(matches)} messages that match rule 0.")


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
