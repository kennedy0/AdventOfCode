import sys

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    card_public, door_public = [int(k) for k in list(read_lines(input_file))]
    card_loop = find_loop_size(public_key=card_public)
    door_loop = find_loop_size(public_key=door_public)
    encryption_key = transform_subject_number(subject_number=door_public, value=1, loop=card_loop)
    print(f"Encryption key: {encryption_key}")
    return 0


def transform_subject_number(subject_number: int, value: int, loop: int) -> int:
    for x in range(loop):
        value *= subject_number
        value %= 20201227
    return value


def find_loop_size(public_key: int) -> int:
    loop_size = 0
    value = 1
    while True:
        value = transform_subject_number(subject_number=7, value=value, loop=1)
        loop_size += 1
        if value == public_key:
            return loop_size


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
