from initials import *

with open('config.ini') as f:
    d = eval(f.read())

l, e, b = [], [], []

if 'labeled_entries' in d.keys():
    b_x, b_y = 100, 30

    if 'buffer_x' in d.keys():
        b_x = d['buffer_x']
    if 'buffer_y' in d.keys():
        b_y = d['buffer_y']

    x, y = 0, 0

    if 'x' in d.keys():
        x = d['x']
    if 'y' in d.keys():
        y = d['y']

    for i in range(len(d['labeled_entries'])):
        l += [tkinter.Label(canvas, text=d['labeled_entries'][i])]
        e += [tkinter.Entry(canvas)]

    for i in l:
        i.place(x=x, y=y)

        y += b_y

    x += b_x; y = d['y']

    for i in e:
        i.place(x=x, y=y)

        y += b_y

btn = [{'label': 'OK', 'x': d['width'] - 120, 'y': d['height'] - 30, 'command': 'b_ok'},
       {'label': 'Cancel', 'x': d['width'] - 70, 'y': d['height'] - 30, 'command': 'b_cancel'}]

if 'buttons' in d.keys():
    btn += d['buttons']

for i in range(len(btn)):
    b += [tkinter.Button(canvas, text=btn[i]['label'], command=btn[i]['command'])]

    b[i].place(x=btn[i]['x'], y=btn[i]['y'])

if 'win_title' in d.keys():
    root.title(d['win_title'])

canvas.pack()
