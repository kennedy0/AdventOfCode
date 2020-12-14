import sys
from collections import defaultdict
from typing import Generator, List, Tuple

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    instructions = list(read_lines(input_file))

    memory_v1 = defaultdict(int)
    memory_v2 = defaultdict(int)
    mask = "X"*36

    for line in instructions:
        if line.startswith("mask"):
            mask = read_mask(text=line)
        elif line.startswith("mem"):
            address, value = read_mem(text=line)
            memory_v1[address] = write_masked_value(value, mask)
            for floating_address in get_floating_addresses(base_address=address, mask=mask):
                memory_v2[floating_address] = value
        else:
            raise RuntimeError

    print(f"Sum of all addresses is {sum(memory_v1.values())} (Using decoder v1)")
    print(f"Sum of all addresses is {sum(memory_v2.values())} (Using decoder v2)")

    return 0


def read_mask(text: str) -> str:
    return text.replace("mask = ", "")


def read_mem(text: str) -> Tuple[int, int]:
    address, value = text.split(" = ")
    address = int(address.strip("mem[]"))
    value = int(value)
    return address, value


def write_masked_value(value: int, mask: str) -> int:
    new_value = []
    value_bin = format(value, '036b')
    for i, bit in enumerate(mask):
        if bit == "X":
            new_value.append(value_bin[i])
        else:
            new_value.append(bit)
    new_value = "".join(new_value)
    return int(new_value, base=2)


def get_floating_addresses(base_address: int, mask: str) -> Generator[int, None, None]:
    base_address_bin = format(base_address, '036b')
    floating_address = []
    for i, bit in enumerate(mask):
        if bit == "0":
            floating_address.append(base_address_bin[i])
        else:
            floating_address.append(bit)
    floating_address = "".join(floating_address)

    floating_digits = mask.count("X")
    combinations = int("1"*floating_digits, base=2)
    for i in range(combinations+1):
        address = floating_address
        i_bin = format(i, f'0{floating_digits}b')
        for bit in i_bin:
            address = address.replace("X", bit, 1)
        yield int(address, base=2)


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
