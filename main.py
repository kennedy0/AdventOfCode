import os
import sys
from types import ModuleType

from dearpygui.core import *
from dearpygui.simple import *

from year_2020.day_01 import day_01
from year_2020.day_02 import day_02
from year_2020.day_03 import day_03
from year_2020.day_04 import day_04
from year_2020.day_05 import day_05
from year_2020.day_06 import day_06
from year_2020.day_07 import day_07
from year_2020.day_08 import day_08
from year_2020.day_09 import day_09


def on_button_click(sender, data):
    module = data  # type: ModuleType
    input_file = os.path.join(os.path.dirname(module.__file__), "input.txt")
    module.main(input_file=input_file)  # noqa


def main() -> int:
    set_main_window_size(width=1280, height=720)
    set_main_window_title("AdventOfCode")

    with window("AdventOfCode"):
        add_button("Day 01", callback=on_button_click, callback_data=day_01)
        add_button("Day 02", callback=on_button_click, callback_data=day_02)
        add_button("Day 03", callback=on_button_click, callback_data=day_03)
        add_button("Day 04", callback=on_button_click, callback_data=day_04)
        add_button("Day 05", callback=on_button_click, callback_data=day_05)
        add_button("Day 06", callback=on_button_click, callback_data=day_06)
        add_button("Day 07", callback=on_button_click, callback_data=day_07)
        add_button("Day 08", callback=on_button_click, callback_data=day_08)
        add_button("Day 09", callback=on_button_click, callback_data=day_09)

    start_dearpygui(primary_window="AdventOfCode")
    return 0


if __name__ == "__main__":
    sys.exit(main())
