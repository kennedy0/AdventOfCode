import sys
from typing import List, Tuple

from utils.input_file import file_path_from_args
from utils.memoize import memoize
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    time, ids = parse_input(input_file)
    find_shortest_wait(time=time, ids=ids)
    find_consecutive_schedule(ids=ids)

    return 0


def parse_input(input_file: str) -> Tuple[int, List]:
    time = int(list(read_lines(input_file))[0])
    ids = list(read_lines(input_file))[1].split(",")
    return time, ids


def is_int(string: str) -> bool:
    """ Check whether a string can resolve to an integer. """
    if not isinstance(string, str):
        return False

    # noinspection PyBroadException
    try:
        int(string)
        return True
    except Exception:
        return False


def find_shortest_wait(time: int, ids: List):
    shortest_wait = None
    bus = None

    for id_ in ids:
        if not is_int(id_):
            continue
        else:
            id_ = int(id_)

        wait = wait_time(time=time, id_=id_)
        if shortest_wait is None or wait < shortest_wait:
            shortest_wait = wait
            bus = id_

    print(f"Bus {bus} departs in {shortest_wait} minutes.  {bus} * {shortest_wait} = {bus * shortest_wait}")


@memoize
def wait_time(time: int, id_: int) -> int:
    departed_last = time % id_  # time since last departure
    if departed_last == 0:
        departs_next = 0
    else:
        departs_next = id_ - departed_last  # time until next departure
    return departs_next


def find_consecutive_schedule(ids: List):
    schedule = list()
    for offset, id_ in enumerate(ids):
        if not is_int(id_):
            continue
        else:
            id_ = int(id_)
        schedule.append((offset, id_))

    # Start at 0
    t = 0
    step = 1

    # For each bus ID in the schedule, find the place where its schedule lines up
    for offset, id_ in schedule:
        while True:
            if (t + offset) % id_ == 0:
                # At time `t` (plus the offset),
                break
            else:
                t += step
        step *= id_

    print(f"Schedule lines up at {t} minutes.")


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
