from __future__ import annotations
import math
import sys
from typing import Dict, List, Generator

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines

SEA_MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]


class Tile:
    def __init__(self, name: str, image: List[str]):
        self.name = name
        self.image = image
        self.north = None
        self.south = None
        self.east = None
        self.west = None

        self.locked = False

    def __str__(self):
        return self.name

    def print_image(self):
        print("\n".join(self.image))

    @property
    def id(self):
        return int(self.name[5:9])

    @property
    def top(self) -> str:
        return self.image[0]

    @property
    def bottom(self) -> str:
        return self.image[-1]

    @property
    def left(self) -> str:
        return "".join([row[0] for row in self.image])

    @property
    def right(self) -> str:
        return "".join([row[-1] for row in self.image])

    def rotate(self):
        new_image = ["" for x in self.image]
        for col in range(len(self.image[0])):
            for row in reversed(range(len(self.image))):
                new_image[col] += self.image[row][col]
        self.image = new_image

    def flip(self):
        for i, line in enumerate(self.image):
            self.image[i] = line[::-1]

    def link(self, other_tile: Tile):
        if self.top == other_tile.bottom:
            self.north = other_tile
            other_tile.south = self
            return True
        elif self.bottom == other_tile.top:
            self.south = other_tile
            other_tile.north = self
            return True
        elif self.right == other_tile.left:
            self.east = other_tile
            other_tile.west = self
            return True
        elif self.left == other_tile.right:
            self.west = other_tile
            other_tile.east = self
            return True
        else:
            return False


def main(input_file: str) -> int:
    unlocked_tiles = get_tiles(file=input_file)

    # Start by choosing one tile to be 'locked' in place
    locked_tiles = []
    t = unlocked_tiles.pop()
    t.locked = True
    locked_tiles.append(t)

    # Go through each 'unlocked' tile and try to fit it into the locked tiles
    while len(unlocked_tiles):
        for tile in unlocked_tiles:
            linked = try_to_link(tiles=locked_tiles, tile=tile)
            if linked:
                locked_tiles.append(tile)
                unlocked_tiles.remove(tile)
                break

    # Part 1
    find_corners(tiles=locked_tiles)

    # Part 2
    combined = combine_tiles(tiles=locked_tiles)
    for x in range(8):
        num_sea_monsters = count_sea_monsters(image=combined.image)
        if num_sea_monsters > 0:
            print(f"Found {num_sea_monsters} sea monsters.")
            break
        combined.rotate()
        if x in [3, 7]:
            combined.flip()

    combined_pixel_count = "".join(combined.image).count("#")
    sea_monster_pixel_count = "".join(SEA_MONSTER).count("#") * num_sea_monsters
    water_roughness = combined_pixel_count - sea_monster_pixel_count
    print(f"Water roughness is {water_roughness}.")
    return 0


def get_tiles(file: str) -> List[Tile]:
    tiles = []

    lines = list(read_lines(file_path=file))
    indicies = [i for i, line in enumerate(lines) if line.startswith("Tile")]
    for i in range(len(indicies)):
        if i == len(indicies)-1:
            slice = lines[indicies[i]:]
            name = slice[0]
            image = slice[1:]
        else:
            slice = lines[indicies[i]:indicies[i+1]]
            name = slice[0]
            image = slice[1:-1]
        tiles.append(Tile(name=name, image=image))

    return tiles


def try_to_link(tiles: List[Tile], tile: Tile):
    """ Try to link a tile with existing tiles.
    Once a link is made, the tile is locked, and can't be rotated/flipped.
    """
    linked = False
    for other_tile in tiles:
        for x in range(8):
            if tile.link(other_tile):
                linked = True
                tile.locked = True
            if tile.locked is True:
                continue
            tile.rotate()
            if x in [3, 7]:
                tile.flip()
    return linked


def find_corners(tiles: List[Tile]):
    top_left = None
    top_right = None
    bottom_left = None
    bottom_right = None
    for tile in tiles:
        if tile.north is None and tile.west is None:
            top_left = tile
        elif tile.north is None and tile.east is None:
            top_right = tile
        elif tile.south is None and tile.west is None:
            bottom_left = tile
        elif tile.south is None and tile.east is None:
            bottom_right = tile

    product = math.prod([top_left.id, top_right.id, bottom_left.id, bottom_right.id])
    print(f"Product of corner tiles is {product}")
    return


def combine_tiles(tiles: List[Tile]) -> Tile:
    # Start with top-left tile
    for tile in tiles:
        if tile.north is None and tile.west is None:
            top_left = tile

    # Build new image that is the combined size of all tiles (minus 2 for the stripped border)
    tile_size = len(top_left.image) - 2
    tile_rows = int(math.sqrt(len(tiles)))
    image = ["" for _ in range(tile_rows * tile_size)]

    # Iterate over each tile (left>right, top>bottom), building the final image.
    row_start = top_left
    tile = top_left
    row_offset = 0
    for _ in range(len(tiles)):
        for i, row in enumerate(tile.image[1:-1]):
            image[i+row_offset] += row[1:-1]
        if tile.east is not None:
            tile = tile.east
        else:
            row_offset += tile_size
            tile = row_start.south
            row_start = tile

    return Tile(name="combined", image=image)


def count_sea_monsters(image: List[str]) -> int:
    count = 0
    sea_monster_width = len(SEA_MONSTER[0])
    sea_monster_height = len(SEA_MONSTER)
    image_size = len(image)

    # Slide SEA_MONSTER kernel across image to look for matches.
    for j in range(image_size-sea_monster_height):
        for i in range(image_size-sea_monster_width):
            image_slice = [row[i:i+sea_monster_width] for row in image[j:j+sea_monster_height]]
            if find_sea_monster(image_slice=image_slice):
                count += 1
    return count


def find_sea_monster(image_slice: List[str]) -> bool:
    """ Compare pixels in an image slice against the SEA_MONSTER to see if it's a match. """
    # Flatten sea monster and image slice into 1d array for easier comparison.
    sea_monster = "".join(SEA_MONSTER)
    image = "".join(image_slice)
    for i, pixel in enumerate(sea_monster):
        if pixel == "#" and image[i] != "#":
            return False
    return True


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
