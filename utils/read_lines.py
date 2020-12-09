from typing import Generator


def read_lines(file_path: str) -> Generator[str, None, None]:
    """ Generator that yields clean lines from 'input.txt'; relative to the current working directory. """
    with open(file_path, 'r') as fp:
        for line in fp.readlines():
            yield line.strip()
