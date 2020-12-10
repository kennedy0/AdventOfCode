from enum import Enum

from dearpygui.core import *
from dearpygui.simple import *


class Theme(Enum):
    Dark = "Dark"
    Light = "Light"
    Classic = "Classic"
    Dark2 = "Dark 2"
    Grey = "Grey"
    DarkGrey = "Dark Grey"
    Cherry = "Cherry"
    Purple = "Purple"
    Gold = "Gold"
    Red = "Red"


def set_style():
    set_theme(Theme.Dark.value)
    set_global_font_scale(1.0)
