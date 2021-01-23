from ui_definitions import *
import pickle
import hmac
import hashlib
import datetime
import os


def b_ok(event=None):
    global e, C, o, m, months

    responses = []

    for i in e:
        responses += [i.get()]

    for i in C:
        for j in i:
            responses += [j.get()]

    for i in o:
        if i.get() == 'None':
            responses += ['None']
        else:
            responses += [eval(i.get())[0]]

    for i in m:
        responses += [i.get('1.0', 'end-1c')]

    if os.path.exists('Storage.dat') and os.path.getsize('Storage.dat'):
        with open('Storage.dat', 'rb+') as f:
            with open('DATA.BIN', 'rb') as g:
                ke = g.read()

            i = f.read()
            if hmac.new(b'shared-key', i, hashlib.sha256).digest() == ke:
                di = eval(pickle.loads(i))
                di[str(datetime.datetime.now().strftime('%d') + datetime.datetime.now().strftime('%m') + datetime.datetime.now().strftime('%Y'))] += [responses]

                x = pickle.dumps(str(di).encode())

                with open('DATA.BIN', 'wb') as g:
                    g.write(hmac.new(b'shared-key', x, hashlib.sha256).digest())

                f.seek(0)
                f.write(x)
    else:
        x = pickle.dumps(str({str(datetime.datetime.now().strftime('%d') + datetime.datetime.now().strftime('%m') + datetime.datetime.now().strftime('%Y')): [responses]}).encode())

        with open('Storage.dat', 'wb') as f:
            f.write(x)

        with open('DATA.BIN', 'wb') as f:
            f.write(hmac.new(b'shared-key', x, hashlib.sha256).digest())

    root.destroy()


def b_cancel():
    root.destroy()
