from ui_definitions import *


def b_ok(event=None):
    global entries

    for i in range(len(l)):
        print(entries[i]['label'], entries[i]['response'].get(), sep=': ')

    root.destroy()


def b_cancel():
    root.destroy()
