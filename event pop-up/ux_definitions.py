from ui_definitions import *


def b_ok(event=None):
    global e

    print(e[0].get())

    root.destroy()

    return True


def b_cancel():
    root.destroy()

    return False
