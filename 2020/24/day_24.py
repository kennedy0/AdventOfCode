import sys
from collections import defaultdict
from typing import List, Tuple, Set

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


DIRECTIONS = {
    'ne': (1, -1),
    'nw': (0, -1),
    'e': (1, 0),
    'w': (-1, 0),
    'se': (0, 1),
    'sw': (-1, 1),
}


class Tiles:
    def __init__(self):
        self.tiles = set()
        self.origin = (0, 0)

    @property
    def black_tiles(self):
        return len(self.tiles)

    def flip(self, x: int, y: int):
        if (x, y) in self.tiles:
            self.tiles.remove((x, y))
        else:
            self.tiles.add((x, y))

    def find_tile(self, instructions: List[str]) -> Tuple[int, int]:
        x, y = self.origin
        for step in instructions:
            i, j = DIRECTIONS[step]
            x += i
            y += j
        return x, y

    def neighbors(self, x: int, y: int) -> Set:
        return set([(x+i, y+j) for i, j in DIRECTIONS.values()])

    def black_neighbors(self, x: int, y: int) -> int:
        return len(self.neighbors(x, y).intersection(self.tiles))

    def is_black(self, x: int, y: int) -> bool:
        return (x, y) in self.tiles

    def all_tiles(self) -> List:
        tiles = set()
        for tile in self.tiles:
            tiles.add(tile)
            tiles.update(self.neighbors(tile[0], tile[1]))
        return list(tiles)

    def next_day(self):
        to_flip = set()
        for x, y in self.all_tiles():
            black_neighbors = self.black_neighbors(x, y)
            if self.is_black(x, y):
                if black_neighbors == 0 or black_neighbors > 2:
                    to_flip.add((x, y))
            elif black_neighbors == 2:
                to_flip.add((x, y))
        for x, y in to_flip:
            self.flip(x, y)


def main(input_file: str) -> int:
    tiles = Tiles()
    for instructions in parse_tiles(file=input_file):
        x, y = tiles.find_tile(instructions)
        tiles.flip(x, y)
    print(f"{tiles.black_tiles} tiles are black.")

    for x in range(100):
        tiles.next_day()

    print(f"{tiles.black_tiles} are black after 100 days.")
    return 0


def parse_tiles(file: str) -> List[List[str]]:
    tiles = []
    for line in read_lines(file):
        i = 0
        instructions = []
        while i < len(line):
            chars = 2 if line[i] in ["n", "s"] else 1
            instructions.append(line[i:i+chars])
            i += chars
        tiles.append(instructions)
    return tiles


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
