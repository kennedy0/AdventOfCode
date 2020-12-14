from __future__ import annotations
import sys
from enum import Enum
from typing import List

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


class State(Enum):
    Floor = "."
    Empty = "L"
    Occupied = "#"

    @staticmethod
    def from_str(s: str) -> State:
        for e in State:  # type: State
            if e.value == s:
                return e


class Grid:
    def __init__(self, file: str):
        self.width = 0
        self.height = 0
        self.rows = []
        self._init_grid(file=file)

    def __str__(self):
        s = ""
        for row in self.rows:
            s += "  ".join([str(c) for c in row]) + "\n"
        return s

    def reset(self):
        for cell in self.cells():
            if cell.state == State.Occupied:
                cell.state = State.Empty

    def _init_grid(self, file: str):
        for j, line in enumerate(read_lines(file)):
            row = []
            for i, char in enumerate(line):
                cell = Cell(x=i, y=j, state=State.from_str(char))
                row.append(cell)
            self.rows.append(row)
        self.height = len(self.rows)
        self.width = len(self.rows[0])

    def get_cell(self, x: int, y: int) -> Cell or None:
        if x in range(self.width) and y in range(self.height):
            return self.rows[y][x]
        else:
            return None

    def get_surrounding(self, cell: Cell) -> List[Cell]:
        for j in range(cell.y-1, cell.y+2):
            for i in range(cell.x-1, cell.x+2):
                if (c := self.get_cell(i, j)) is not None:
                    if c != cell:
                        yield c

    def get_line_of_sight(self, cell: Cell) -> List[Cell]:
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for i, j in directions:
            x = cell.x + i
            y = cell.y + j
            while True:
                c = self.get_cell(x, y)
                if c is None:
                    break
                elif c.state == State.Floor:
                    x += i
                    y += j
                    continue
                else:
                    break

            if c is not None:
                yield c

    def cells(self) -> List[Cell]:
        for row in self.rows:
            for cell in row:  # type: Cell
                yield cell

    def advance_round(self, neighbors_tolerated: int, search_method: str):
        new_rows = []
        for row in self.rows:
            new_row = []
            for cell in row:
                if search_method == "neighbors":
                    neighbor_states = [c.state for c in self.get_surrounding(cell)]
                elif search_method == "line of sight":
                    neighbor_states = [c.state for c in self.get_line_of_sight(cell)]
                else:
                    raise NotImplementedError(search_method)

                if cell.state == State.Empty and State.Occupied not in neighbor_states:
                    new_row.append(Cell(cell.x, cell.y, State.Occupied))
                elif cell.state == State.Occupied and neighbor_states.count(State.Occupied) > neighbors_tolerated:
                    new_row.append(Cell(cell.x, cell.y, State.Empty))
                else:
                    new_row.append(cell)
            new_rows.append(new_row)

        self.rows = new_rows


class Cell:
    def __init__(self, x: int, y: int, state: State):
        self.x = x
        self.y = y
        self.state = state

    def __str__(self):
        return self.state.value


def main(input_file: str) -> int:
    grid = Grid(file=input_file)
    stabilize(grid=grid, leave_at=4, search_method="neighbors")
    stabilize(grid=grid, leave_at=5, search_method="line of sight")
    return 0


def stabilize(grid: Grid, leave_at: int, search_method: str):
    grid.reset()
    previous_state = None
    counter = 0
    while (current_state := str(grid)) != previous_state:
        previous_state = current_state
        grid.advance_round(neighbors_tolerated=leave_at-1, search_method=search_method)
        counter += 1

    stabilization = counter - 1
    occupied = len([c for c in grid.cells() if c.state == State.Occupied])

    print(f"Seats stabilized after {stabilization} rounds (search method: {search_method}).")
    print(f"{occupied} seats are occupied.")


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
