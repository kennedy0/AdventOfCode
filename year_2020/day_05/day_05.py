from __future__ import annotations

import sys
from enum import Enum
from typing import List

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


class Direction(Enum):
    Left = "Left"
    Right = "Right"


class Node:
    def __init__(self, parent: Node or None, values: List[int]):
        self.parent = parent
        self._children = []
        self.values = values

        if isinstance(self.parent, Node):
            self.parent.add_child(self)

    def add_child(self, child: Node):
        if len(self._children) >= 2:
            raise RuntimeError("Nodes in a Binary Tree cannot have more than 2 children.")
        self._children.append(child)

    def get_child(self, direction: Direction) -> Node:
        if direction == Direction.Left:
            return self._children[0]
        elif direction == Direction.Right:
            return self._children[1]
        else:
            raise RuntimeError(f"Invalid Direction: {Direction}")


class BinaryTree:
    def __init__(self, data_set: List):
        self.root = Node(parent=None, values=data_set)
        self.build_child_nodes(node=self.root)

    def build_child_nodes(self, node: Node):
        if len(node.values) > 1:
            index = int(len(node.values) / 2)

            left_values = node.values[:index]
            right_values = node.values[index:]

            child_left = Node(parent=node, values=left_values)
            child_right = Node(parent=node, values=right_values)

            self.build_child_nodes(node=child_left)
            self.build_child_nodes(node=child_right)

    def traverse(self, instructions: str, left: str = "L", right: str = "R") -> int or List[int]:
        direction_map = {left: Direction.Left, right: Direction.Right}

        node = self.root
        for char in instructions:
            node = node.get_child(direction=direction_map[char])

        return node.values


ROW_TREE = BinaryTree(data_set=list(range(128)))
COL_TREE = BinaryTree(data_set=list(range(8)))


class BoardingPass:
    def __init__(self, text: str):
        self.text = text
        self.row = None
        self.column = None
        self._parse_text()
    
    def __str__(self):
        return f"{self.text}: row {self.row}, column {self.column}, seat ID {self.seat_id}"
    
    @property
    def seat_id(self):
        return (self.row * 8) + self.column

    def _parse_text(self):
        row = ROW_TREE.traverse(instructions=self.text[:7], left="F", right="B")
        col = COL_TREE.traverse(instructions=self.text[7:])
        self.row = row[0]
        self.column = col[0]


def main(input_file: str) -> int:
    boarding_passes = []
    for line in read_lines(input_file):
        boarding_passes.append(BoardingPass(text=line))

    seat_ids = sorted([bp.seat_id for bp in boarding_passes])
    print(f"Highest seat ID is {max(seat_ids)}")

    for seat_id in seat_ids:
        if seat_id + 1 not in seat_ids:
            print(f"Seat ID {seat_id + 1} is missing.")
            break
    return 0


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
