from ui_definitions import *
import pickle
import hmac
import hashlib


def b_ok(event=None):
    global e, C, o, m, months

    responses = []

    for i in e:
        responses += [i.get()]

    for i in C:
        for j in i:
            responses += [j.get()]

    for i in o:
        responses += [eval(i.get())[0]]

    for i in m:
        responses += [i.get('1.0', 'end-1c')]

    x = pickle.dumps(str(responses))

    with open('DATA.BIN', 'wb') as f:
        f.write(hmac.new(b'shared-key', x, hashlib.sha256).digest())

    with open('Storage.dat', 'wb') as f:
        f.write(x)

    root.destroy()


def b_cancel():
    root.destroy()
