import re
import sys
from enum import Enum

from utils.input_file import file_path_from_args
from utils.print_fn import print
from utils.read_lines import read_lines


password_re = re.compile(
    r"^(?P<policy_min>[\d]+)-(?P<policy_max>[\d]+)\s(?P<policy_letter>[\w]):\s(?P<password>[\w]+)$",
    re.I)


class Policy(Enum):
    Count = "Count"
    Position = "Position"


class Password:
    def __init__(self, text: str, policy: Policy):
        self._policy = policy

        self._policy_num_a = None
        self._policy_num_b = None
        self._policy_letter = None
        self._password = None

        self._parse_text(text=text)

    def _parse_text(self, text: str):
        match = re.match(password_re, text)
        self._policy_num_a = int(match.group('policy_min'))
        self._policy_num_b = int(match.group('policy_max'))
        self._policy_letter = match.group('policy_letter')
        self._password = match.group('password')

    @property
    def valid(self) -> bool:
        if self._policy == Policy.Count:
            return self.validate_policy_count()
        elif self._policy == Policy.Position:
            return self.validate_policy_position()

    def validate_policy_count(self) -> bool:
        min_count = self._policy_num_a
        max_count = self._policy_num_b
        count = self._password.count(self._policy_letter)
        if min_count <= count <= max_count:
            return True
        else:
            return False

    def validate_policy_position(self) -> bool:
        index_1 = self._policy_num_a - 1
        index_2 = self._policy_num_b - 1
        letters = [self._password[index_1], self._password[index_2]]
        if letters.count(self._policy_letter) == 1:
            return True
        else:
            return False


def main(input_file: str) -> int:
    for policy in Policy:
        passwords = []
        for line in read_lines(input_file):
            passwords.append(Password(text=line, policy=policy))

        valid_passwords = [p for p in passwords if p.valid]
        print(f"{len(valid_passwords)} out of {len(passwords)} are valid (using policy: {policy.value})")

    return 0


if __name__ == "__main__":
    sys.exit(main(input_file=file_path_from_args()))
