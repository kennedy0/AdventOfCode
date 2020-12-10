""" Lasciate ogni speranza, voi ch'entrate """

from dearpygui.core import *

_print = print


def custom_print(*args, **kwargs):
    _print(*args, **kwargs)
    log_info(message=f"{' '.join([str(a) for a in args])}", logger="Console")


print = custom_print
