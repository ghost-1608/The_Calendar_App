from ui_definitions import *
import pickle
import hmac
import hashlib


def b_ok(event=None):
    global responses

    for i in range(len(responses)):
        for j in range(len(responses[i])):
            if 'list' not in str(type(responses[i][j])):
                if i == 3:
                    responses[i][j] = responses[i][j].get('1.0', 'end-1c')
                else:
                    responses[i][j] = responses[i][j].get()
            else:
                for k in range(len(responses[i][j])):
                    responses[i][j][k] = responses[i][j][k].get()

    x = pickle.dumps(str(responses))

    with open('KEY.BIN', 'wb') as f:
        f.write(hmac.new(b'shared-key', x, hashlib.sha256).digest())

    with open('data.dat', 'wb') as f:
        f.write(x)

    root.destroy()


def b_cancel():
    root.destroy()
