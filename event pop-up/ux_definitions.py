from ui_definitions import *
import pickle


def b_ok(event=None):
    global responses

    with open('data.dat', 'wb') as f:
        pickle.dump(str(responses), f)

    root.destroy()


def b_cancel():
    root.destroy()
