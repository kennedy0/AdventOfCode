import sys
from typing import List

from utils.input_file import file_path_from_args
from utils.print_fn import print
from utils.read_lines import read_lines


class Passport:
    def __init__(self, text: str):
        self.data = dict()
        self.fields = {
            'byr': {'name': "Birth Year", 'required': True, 'validator': self.validate_byr},
            'iyr': {'name': "Issue Year", 'required': True, 'validator': self.validate_iyr},
            'eyr': {'name': "Expiration Year", 'required': True, 'validator': self.validate_eyr},
            'hgt': {'name': "Height", 'required': True, 'validator': self.validate_hgt},
            'hcl': {'name': "Hair Color", 'required': True, 'validator': self.validate_hcl},
            'ecl': {'name': "Eye Color", 'required': True, 'validator': self.validate_ecl},
            'pid': {'name': "Passport ID", 'required': True, 'validator': self.validate_pid},
            'cid': {'name': "Country ID", 'required': False, 'validator': self.validate_cid},
        }

        self._parse_text(text=text)

    def _parse_text(self, text: str):
        for pairs in text.split(" "):
            key, value = pairs.split(":")
            self.data.update({key: value})

    @property
    def valid(self) -> bool:
        if self.validate_required_fields() is False:
            return False
        for key, value in self.data.items():
            validate_fn = self.fields[key]['validator']
            if validate_fn(value) is False:
                return False
        return True

    def validate_required_fields(self) -> bool:
        for field, field_info in self.fields.items():
            if field_info['required'] is True and field not in self.data.keys():
                return False
        return True

    def validate_byr(self, value: str) -> bool:
        if len(value) == 4:
            if 1920 <= int(value) <= 2002:
                return True
        return False

    def validate_iyr(self, value: str) -> bool:
        if len(value) == 4:
            if 2010 <= int(value) <= 2020:
                return True
        return False

    def validate_eyr(self, value: str) -> bool:
        if len(value) == 4:
            if 2020 <= int(value) <= 2030:
                return True
        return False

    def validate_hgt(self, value: str) -> bool:
        unit = value[-2:]
        if unit == "cm":
            valid_range = 150, 193
        elif unit == "in":
            valid_range = 59, 76
        else:
            return False

        height = int(value[:-2])
        if valid_range[0] <= height <= valid_range[1]:
            return True
        else:
            return False

    def validate_hcl(self, value: str) -> bool:
        if not value.startswith("#"):
            return False

        color = value[1:]
        if not len(color) == 6:
            return False

        for char in color:
            if char not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]:
                return False

        return True

    def validate_ecl(self, value: str) -> bool:
        if value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return True
        else:
            return False

    def validate_pid(self, value: str) -> bool:
        try:
            assert len(value) == 9
            int(value)
            return True
        except Exception:
            return False

    def validate_cid(self, value: str) -> bool:
        return True


def main(input_file: str) -> int:
    passports = get_passport_list(file=input_file)
    valid_passports = [p for p in passports if p.valid]
    print(f"Found {len(valid_passports)} valid passports (out of {len(passports)})")
    return 0


def get_passport_list(file: str) -> List[Passport]:
    passports = list()

    # Group lines
    line_groups = []
    text_group = []
    for line in read_lines(file_path=file):
        if line == "":
            line_groups.append(text_group)
            text_group = []
            continue
        else:
            text_group.append(line)

    if len(text_group):
        # Last group
        line_groups.append(text_group)

    for text_group in line_groups:
        passport_data_text = " ".join(text_group)
        passports.append(Passport(text=passport_data_text))

    return passports


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
