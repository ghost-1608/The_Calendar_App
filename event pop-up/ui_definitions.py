from initials import *
import tkinter.scrolledtext
from tkinter import ttk


def return_handle(event):
    global days

    for i in [e, c, de, m]:
        if root.focus_get() in i:
            break

    if i == e:
        pass
    if i == c:
        if c[-1].get() and c[-1].get() not in days:
            c[-1].set('')
    if i == de:
        pass
    if i == m:
        pass


l, e, c, d, m = [], [], [], [], []

b_x, b_y = 100, 40

X, Y = 10, 50

event_name = {'label': tkinter.Label(canvas, text='Event Name: '), 'entry': tkinter.Entry(canvas)}
l += [event_name['label']]
e += [event_name['entry']]

tags = {'label': tkinter.Label(canvas, text='Tags: '), 'entry': tkinter.Entry(canvas)}
l += [tags['label']]
e += [tags['entry']]

days = [str(i) for i in range(1, 32)]
vals = days
n = tkinter.StringVar()
date = {'label': tkinter.Label(canvas, text='Dates: '),
        'value': tkinter.ttk.Combobox(canvas, width=2, textvariable=n)}
date['value']['values'] = vals
l += [date['label']]
c += [date['value']]


v = tkinter.StringVar(root)
v.set('None')
repeat_select = {'label': tkinter.Label(canvas, text='Repeat: '),
                 'value': tkinter.OptionMenu(root, v, ['None'], ['Daily'], ['Weekly'], ['Monthly'], ['Yearly'])}
repeat_select['value'].configure(takefocus=True)
l += [repeat_select['label']]
d += [repeat_select['value']]

multi_textbox = {'label': tkinter.Label(canvas, text='Description: '),
                 'entry': tkinter.scrolledtext.ScrolledText(canvas)}
l += [multi_textbox['label']]
m += [multi_textbox['entry']]

x, y = X, Y

for i in l:
    i.place(x=x, y=y)
    y += b_y

y = Y; x += b_x

for i in e:
    i.place(x=x, y=y)
    y += b_y

for i in c:
    i.place(x=x, y=y)
    y += b_y

for i in d:
    i.place(x=x, y=y)
    y += b_y

for i in m:
    i.place(x=x, y=y)
    y += b_y

if 'win_title' in de.keys():
    root.title(de['win_title'])

if 'win_icon' in de.keys():
    root.iconphoto(False, tkinter.PhotoImage(de['win_icon']))

root.bind('<Return>', return_handle)

canvas.pack()
