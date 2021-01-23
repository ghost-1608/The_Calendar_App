from initials import *
import tkinter.scrolledtext
from tkinter import ttk


def return_handle(event):
    global days, e, c, d, m

    if i in e:
        pass
    if i in c:
        pass
    if i in d:
        pass
    if i in m:
        pass


l, e, c, C, d, o, m = [], [], [], [], [], [], []

b_x, b_y = 100, 40

X, Y = 10, 50

event_name = {'label': tkinter.Label(canvas, text='Event Name: '), 'entry': tkinter.Entry(canvas)}
l += [event_name['label']]
e += [event_name['entry']]

tags = {'label': tkinter.Label(canvas, text='Tags: '), 'entry': tkinter.Entry(canvas)}
l += [tags['label']]
e += [tags['entry']]

days = [str(i) for i in range(1, 32)]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = [str(i) for i in range(1900, 2101)]
n = [tkinter.StringVar() for i in range(3)]
date = {'label': tkinter.Label(canvas, text='Dates: '),
        'value': [tkinter.ttk.Combobox(canvas, state='readonly', width=2, textvariable=n[0]),
                  tkinter.ttk.Combobox(canvas, state='readonly', width=10, textvariable=n[1]),
                  tkinter.ttk.Combobox(canvas, state='readonly', width=4, textvariable=n[2])]}
date['value'][0]['values'] = days
date['value'][1]['values'] = months
date['value'][2]['values'] = years
l += [date['label']]
c += [date['value']]
C += [n]

v = tkinter.StringVar(canvas)
v.set('None')
repeat_select = {'label': tkinter.Label(canvas, text='Repeat: '),
                 'value': tkinter.OptionMenu(canvas, v, ['None'], ['Daily'], ['Weekly'], ['Monthly'], ['Yearly'])}
repeat_select['value'].configure(takefocus=True)
# repeat_select['value'].configure(bg=bg)
l += [repeat_select['label']]
d += [repeat_select['value']]
o += [v]

multi_textbox = {'label': tkinter.Label(canvas, text='Description: '),
                 'entry': tkinter.scrolledtext.ScrolledText(canvas, width=50, height=10)}
l += [multi_textbox['label']]
m += [multi_textbox['entry']]

x, y = X, Y

for i in l:
    i.place(x=x, y=y)
    y += b_y

y = Y; x += b_x

for i in e:
    i.place(x=x, y=y + 2)
    y += b_y

for i in c:
    tkinter.Label(canvas, text='DD:').place(x=x, y=y)
    i[0].place(x=x + 35, y=y)
    tkinter.Label(canvas, text='M:').place(x=x + 90, y=y)
    i[1].place(x=x + 120, y=y)
    tkinter.Label(canvas, text='YYYY:').place(x=x + 220, y=y)
    i[2].place(x=x + 270, y=y)
    y += b_y

for i in d:
    i.place(x=x - 2, y=y - 5)
    y += b_y

for i in m:
    i.place(x=x, y=y + 2)
    y += b_y

if 'win_title' in de.keys():
    root.title(de['win_title'])

if 'win_icon' in de.keys():
    root.iconphoto(False, tkinter.PhotoImage(de['win_icon']))

root.bind('<Return>', return_handle)

canvas.pack()
