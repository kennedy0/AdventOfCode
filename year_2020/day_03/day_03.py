import math
import sys
from collections import namedtuple
from typing import List

from utils.input_file import file_path_from_args
from utils.print_fn import print
from utils.read_lines import read_lines


Vector2 = namedtuple("Vector2", "x y")


class TreeMap:
    SQUARE_OPEN = "."
    SQUARE_TREE = "#"

    def __init__(self, input_file: str):
        self.rows = list()
        self.width = 0
        self.path = ""

        self._parse_input_file(file=input_file)

    def _parse_input_file(self, file: str):
        for line in read_lines(file):
            self.rows.append(line)
            if len(line) > self.width:
                self.width = len(line)

    def get_square(self, row: List[str], position: int):
        index = position
        while index >= self.width:
            index -= self.width
        return row[index]

    def tree_count(self, start_position: int, slope: Vector2) -> int:
        path = ""

        position = start_position
        tree_count = 0
        for row in self.rows[::slope.y]:
            # Actual calculation here
            square = self.get_square(row=row, position=position)
            if square == self.SQUARE_TREE:
                tree_count += 1

            # Path for debugging
            if square == self.SQUARE_TREE:
                position_marker = "X"
            else:
                position_marker = "O"
            row_str = row * math.ceil(position / self.width)
            path += f"{row_str[0:position]}{position_marker}{row_str[position+1:]}\n"

            # Increment position
            position += slope.x

        self.path = path
        return tree_count


def main(input_file: str) -> int:
    tree_map = TreeMap(input_file=input_file)

    slopes = [
        Vector2(1, 1),
        Vector2(3, 1),
        Vector2(5, 1),
        Vector2(7, 1),
        Vector2(1, 2),
    ]

    results = list()
    for slope in slopes:
        tree_count = tree_map.tree_count(start_position=0, slope=slope)
        results.append(tree_count)
        print(f"Slope ({slope.x}, {slope.y}) Encountered {tree_count} trees.")

    results_str = " * ".join(str(r) for r in results)
    print(f"{results_str} = {math.prod(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
