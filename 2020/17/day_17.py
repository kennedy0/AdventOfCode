import sys
from collections import namedtuple
from typing import Set

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


ACTIVE = "#"
INACTIVE = "."


Vector3 = namedtuple("Vector3", "x y z")
Vector4 = namedtuple("Vector4", "x y z w")


class Grid3D:
    def __init__(self, input_file: str):
        self.active_cubes = set()

        self.birth_rate = 3
        self.death_rate = [2, 3]

        self._parse_input(file=input_file)

    def _parse_input(self, file: str):
        lines = list(read_lines(file))
        for j, row in enumerate(lines):
            for i, cube in enumerate(row):
                if cube == ACTIVE:
                    self.active_cubes.add(Vector3(i, j, 0))

    @staticmethod
    def neighboring_cubes(cube: Vector3) -> Set[Vector3]:
        cubes = set(Vector3(cube.x+i, cube.y+j, cube.z+k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1))
        cubes.discard(cube)
        return cubes

    def inactive_cubes(self) -> Set[Vector3]:
        """ Return the inactive cubes that are neighbors to the active ones. """
        inactive = set()
        for cube in list(self.active_cubes):
            # Get neighboring cubes that are not in the 'active_cubes' set
            inactive.update(self.neighboring_cubes(cube).difference(self.active_cubes))
        return inactive

    def cycle(self):
        # Check for active cubes that should deactivate
        deactivate = set()
        for cube in list(self.active_cubes):
            active_neighbors = len(self.neighboring_cubes(cube).intersection(self.active_cubes))
            if active_neighbors not in self.death_rate:
                deactivate.add(cube)

        # Check for inactive cubes that should activate
        activate = set()
        for cube in list(self.inactive_cubes()):
            active_neighbors = len(self.neighboring_cubes(cube).intersection(self.active_cubes))
            if active_neighbors == self.birth_rate:
                activate.add(cube)

        # Update active cubes
        self.active_cubes.update(activate)
        self.active_cubes.difference_update(deactivate)

    def run_cycles(self, cycles: int):
        for x in range(cycles):
            self.cycle()


class Grid4D(Grid3D):
    def _parse_input(self, file: str):
        lines = list(read_lines(file))
        for j, row in enumerate(lines):
            for i, cube in enumerate(row):
                if cube == ACTIVE:
                    self.active_cubes.add(Vector4(i, j, 0, 0))

    @staticmethod
    def neighboring_cubes(cube: Vector4) -> Set[Vector4]:
        cubes = set(Vector4(cube.x+i, cube.y+j, cube.z+k, cube.w+l) for i in (-1,0,1) for j in (-1,0,1) for k in (-1,0,1) for l in (-1,0,1))  # noqa
        cubes.discard(cube)
        return cubes


def main(input_file: str) -> int:
    cycles = 6

    grid_3d = Grid3D(input_file=input_file)
    grid_4d = Grid4D(input_file=input_file)

    grid_3d.run_cycles(cycles)
    grid_4d.run_cycles(cycles)

    print(f"{len(grid_3d.active_cubes)} cubes are active after {cycles} cycles (3D Grid).")
    print(f"{len(grid_4d.active_cubes)} cubes are active after {cycles} cycles (4D Grid).")

    return 0


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
