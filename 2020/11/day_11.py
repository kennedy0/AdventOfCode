from __future__ import annotations
import sys
from copy import deepcopy
from typing import Generator, Tuple

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."


class Grid:
    def __init__(self, input_file: str):
        self.grid = []
        self.width = 0
        self.height = 0

        self._updates = []

        self._parse_input(file=input_file)

    def _parse_input(self, file: str):
        grid = []
        for i, line in enumerate(read_lines(file), start=1):
            grid.append([c for c in line])
            self.height = i
            self.width = len(line)
        self.grid = grid

    @property
    def occupied(self) -> int:
        return [s for i, j, s in self.seats()].count(OCCUPIED)

    def seats(self) -> Generator[Tuple[int, int, str], None, None]:
        for j in range(self.height):
            for i in range(self.width):
                yield i, j, self.grid[j][i]

    def occupied_neighbors(self, x: int, y: int, skip_floor: bool, limit: int) -> int:
        occupied = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if not (dx == 0 and dy == 0):
                    i = x + dx
                    j = y + dy
                    if i in range(self.width) and j in range(self.height) and not (i == x and j == y):
                        if skip_floor is True:
                            while i in range(0, self.width) and j in range(0, self.height) and self.grid[j][i] == FLOOR:
                                i += dx
                                j += dy
                        if i in range(self.width) and j in range(self.height) and self.grid[j][i] == OCCUPIED:
                            occupied += 1
                            if occupied >= limit:
                                return occupied
        return occupied

    def set_seat(self, x: int, y: int, state: str):
        self._updates.append((x, y, state))

    def update(self):
        for i, j, seat in self._updates:
            self.grid[j][i] = seat
        self._updates = []


def main(input_file: str) -> int:
    grid_1 = Grid(input_file=input_file)
    grid_2 = deepcopy(grid_1)

    stabilize(grid=grid_1, skip_floor=False, occupied_threshold=4)
    stabilize(grid=grid_2, skip_floor=True, occupied_threshold=5)

    return 0


def stabilize(grid: Grid, skip_floor: bool, occupied_threshold: int):
    stabilized = False
    num_rounds = 0

    while stabilized is False:
        num_rounds += 1
        stabilized = True

        for i, j, seat in grid.seats():
            if seat == FLOOR:
                continue
            elif seat == EMPTY:
                occupied = grid.occupied_neighbors(x=i, y=j, skip_floor=skip_floor, limit=1)
                if occupied == 0:
                    grid.set_seat(x=i, y=j, state=OCCUPIED)
                    stabilized = False
            elif seat == OCCUPIED:
                occupied = grid.occupied_neighbors(x=i, y=j, skip_floor=skip_floor, limit=occupied_threshold)
                if occupied >= occupied_threshold:
                    grid.set_seat(x=i, y=j, state=EMPTY)
                    stabilized = False
        grid.update()

    print(f"Seats stabilized after {num_rounds} rounds with {grid.occupied} occupied seats. (Skip floor: {skip_floor})")


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
