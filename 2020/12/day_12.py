from __future__ import annotations
import math
import sys
from typing import Generator, List, Tuple

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


class Vector2:
    def __init__(self, x: int or float, y: int or float):
        self.x = int(round(x))
        self.y = int(round(y))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(x=self.x+other.x, y=self.y+other.y)

    def __radd__(self, other: Vector2) -> Vector2:
        return self.__add__(other)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(x=self.x-other.x, y=self.y-other.y)

    def __rsub__(self, other: Vector2) -> Vector2:
        return Vector2(x=other.x-self.x, y=other.y-self.y)

    def __mul__(self, other: int or Vector2) -> Vector2:
        if isinstance(other, int):
            return Vector2(x=self.x*other, y=self.y*other)
        elif isinstance(other, Vector2):
            return Vector2(x=self.x*other.x, y=self.y*other.y)
        else:
            raise TypeError

    def __rmul__(self, other: int or Vector2) -> Vector2:
        return self.__mul__(other)

    @classmethod
    def zero(cls) -> Vector2:
        return Vector2(x=0, y=0)


NORTH = Vector2(x=0, y=1)
SOUTH = Vector2(x=0, y=-1)
EAST = Vector2(x=1, y=0)
WEST = Vector2(x=-1, y=0)
DIRECTIONS = {
    'N': NORTH,
    'S': SOUTH,
    'E': EAST,
    'W': WEST,
}


def main(input_file: str) -> int:
    instructions = list(parse_instructions(input_file=input_file))
    absolute_position = navigate_absolute(instructions)
    waypoint_position = navigate_waypoint(instructions)

    print(f"Manhattan Distance (absolute navigation): {manhattan_distance(Vector2.zero(), absolute_position)}")
    print(f"Manhattan Distance (waypoint navigation): {manhattan_distance(Vector2.zero(), waypoint_position)}")

    return 0


def navigate_absolute(instructions: List[Tuple[str, int]]) -> Vector2:
    start_position = Vector2.zero()
    position = start_position
    facing = EAST

    for action, value in instructions:
        if action in DIRECTIONS.keys():
            # Move absolute
            position = move(position=position, direction=DIRECTIONS.get(action), distance=value)
        elif action in ["L", "R"]:
            # Rotate
            facing = rotate(facing_direction=facing, rotation=action, degrees=value)
        elif action == "F":
            # Move relative
            position = move(position=position, direction=facing, distance=value)
        else:
            raise ValueError(action)

    return position


def navigate_waypoint(instructions: List[Tuple[str, int]]) -> Vector2:
    start_position = Vector2.zero()
    position = start_position
    waypoint = start_position + Vector2(x=10, y=1)

    for action, value in instructions:
        if action in DIRECTIONS.keys():
            # Move waypoint
            waypoint = move(position=waypoint, direction=DIRECTIONS.get(action), distance=value)
        elif action in ["L", "R"]:
            # Rotate waypoint around plane
            waypoint = rotate_around(position=waypoint, reference_point=position, rotation=action, degrees=value)
        elif action == "F":
            # Move towards waypoint
            offset = waypoint - position
            position += offset * value
            waypoint += offset * value
        else:
            raise ValueError(action)

    return position


def parse_instructions(input_file: str) -> Generator[Tuple[str, int]]:
    for line in read_lines(input_file):
        yield line[0], int(line[1:])


def move(position: Vector2, direction: Vector2, distance: int) -> Vector2:
    return position + (direction * distance)


def rotate(facing_direction: Vector2, rotation: str, degrees: int) -> Vector2:
    directions = [NORTH, EAST, SOUTH, WEST]
    index = directions.index(facing_direction)
    offset = {'L': -1, 'R': 1}.get(rotation) * int(degrees / 90)
    new_index = (index + offset) % len(directions)
    return directions[new_index]


def rotate_around(position: Vector2, reference_point: Vector2, rotation: str, degrees: int) -> Vector2:
    rel_pos = position - reference_point

    angle = math.radians(degrees if rotation == "L" else -degrees)
    new_x = (math.cos(angle) * rel_pos.x) - (math.sin(angle) * rel_pos.y)
    new_y = (math.sin(angle) * rel_pos.x) + (math.cos(angle) * rel_pos.y)

    rotated_rel_pos = Vector2(x=new_x, y=new_y)
    rotated_pos = reference_point + rotated_rel_pos

    return rotated_pos


def manhattan_distance(pos_a: Vector2, pos_b: Vector2) -> int:
    distance = pos_b - pos_a
    return abs(distance.x) + abs(distance.y)


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
