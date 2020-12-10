import os

from dearpygui.core import *
from dearpygui.simple import *

from .print_fn import print
from .program import Program


class Pr0Gr4m:
    def __init__(self):
        self.program = Program()

        self.run_btn = "run »»"
        self.step_btn = "step »"
        self.window = "pr0gr4m##window"
        self.accumulator = "##Accumulator"
        self.address = "##Address"
        self.instructions = "instructions"
        self.history = "history"

    def init_ui(self):
        with window(self.window, height=475, width=600, no_resize=True, x_pos=720, y_pos=5):
            with menu_bar("menu##program"):
                with menu("file##program"):
                    add_menu_item("load instructions...", callback=self.on_load_instructions)

            with group("group_accumulator", width=200):
                add_text("accumulator", color=[255, 0, 255, 255])
                add_same_line()
                add_input_text(name=self.accumulator, default_value=str(self.program.accumulator), readonly=True)

            add_same_line()
            with group("group_address", width=200):
                add_text("address", color=[255, 255, 128, 255])
                add_same_line()
                add_input_text(name=self.address, default_value=str(self.program.accumulator), readonly=True)

            add_table(self.instructions, headers=["address", "instruction"], height=375, width=200)
            add_same_line()
            add_table(self.history, headers=["history"], height=375, width=100)

            add_button(self.run_btn, callback=self.on_run, enabled=False, width=300)
            set_item_color(self.run_btn, style=21, color=[0, 128, 0, 255])
            add_same_line()
            add_button(self.step_btn, callback=self.step, enabled=False, width=300)
            set_item_color(self.step_btn, style=21, color=[0, 0, 128, 255])


    def on_load_instructions(self, sender, data):
        open_file_dialog(callback=self.load_instructions, extensions=".txt")
        configure_item(self.run_btn, enabled=True)
        configure_item(self.step_btn, enabled=True)

    def load_instructions(self, sender, data):
        path, file = data
        self.program.load_instructions(file=os.path.join(path, file))

        clear_table(self.instructions)
        for i, instruction in enumerate(self.program.instructions, start=1):
            insert_row(self.instructions, row_index=i, row=[str(i), str(instruction)])

    def refresh_history(self):
        clear_table(self.history)
        for instruction in reversed(self.program.visited_addresses):
            insert_row(self.history, row_index=0, row=[str(instruction)])

    def step(self, sender=None, data=None):
        self.program.step()
        set_value(self.accumulator, str(self.program.accumulator))
        set_value(self.address, str(self.program.address))
        self.refresh_history()

    def on_run(self, sender, data):
        run_async_function(self.run, None)

    def run(self, sender, data):
        self.program.reset()
        while self.program.address < len(self.program.instructions):
            run_async_function(self.step, None)

    def boot(self):
        self.init_ui()
