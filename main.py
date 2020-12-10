import os
import sys
from types import ModuleType

from dearpygui.core import *
from dearpygui.simple import *

from utils.style import set_style
from utils.pr0gr4m import Pr0Gr4m

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
    clear_console()
    module = data  # type: ModuleType
    input_file = os.path.join(os.path.dirname(module.__file__), "input.txt")
    module.main(input_file=input_file)  # noqa


def clear_console(sender=None, data=None):
    clear_log(logger="Console")


def on_run_progr4m(sender, data):
    program = Pr0Gr4m()
    program.boot()


def main() -> int:
    set_main_window_size(width=1400, height=720)
    set_main_window_title("AdventOfCode")

    with window("AdventOfCode"):
        with group("Buttons"):
            add_button("Day 01", width=100, callback=on_button_click, callback_data=day_01)
            add_button("Day 02", width=100, callback=on_button_click, callback_data=day_02)
            add_button("Day 03", width=100, callback=on_button_click, callback_data=day_03)
            add_button("Day 04", width=100, callback=on_button_click, callback_data=day_04)
            add_button("Day 05", width=100, callback=on_button_click, callback_data=day_05)
            add_button("Day 06", width=100, callback=on_button_click, callback_data=day_06)
            add_button("Day 07", width=100, callback=on_button_click, callback_data=day_07)
            add_button("Day 08", width=100, callback=on_button_click, callback_data=day_08)
            add_button("Day 09", width=100, callback=on_button_click, callback_data=day_09)
            add_button("Day 10", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 11", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 12", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 13", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 14", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 15", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 16", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 17", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 18", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 19", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 20", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 21", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 22", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 23", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 24", width=100, callback=on_button_click, callback_data=None, enabled=False)
            add_button("Day 25", width=100, callback=on_button_click, callback_data=None, enabled=False)

            add_button("Run pr0gr4m...", width=100, callback=on_run_progr4m)
            set_item_color("Run pr0gr4m...", style=21, color=[255, 0, 0, 255])

        add_same_line()
        with group("Console##Group"):
            add_logger(
                "Console",
                filter=False,
                auto_scroll_button=False,
                clear_button=False,
                copy_button=False,
                width=600,
                height=571)
            clear_console()
            add_button("Clear Console", width=get_item_width("Console"), callback=clear_console)

    set_style()
    start_dearpygui(primary_window="AdventOfCode")
    return 0


if __name__ == "__main__":
    sys.exit(main())
