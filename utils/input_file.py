import os
import sys


def file_path_from_args() -> str:
    if len(sys.argv) < 2:
        file = os.path.join(os.path.dirname(sys.argv[0]), "input.txt")
    else:
        file = sys.argv[1]
    return file
