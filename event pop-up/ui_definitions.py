from initials import *

l = [tkinter.Label(root, text='placeholder1'), tkinter.Label(root, text='placeholder2')]
e = [tkinter.Entry(root), tkinter.Entry(root)]

y = 10

for i in l:
	i.place(x=50, y=y)
	y += 30

y = 10

for i in e:
	i.place(x=150, y=y)
	y += 30

b = [tkinter.Button(root, text='OK', command=b_ok), tkinter.Button(root, text='Cancel', command=b_cancel)]

x, y = [480, 520], [250, 250]

for i in range(len(b)):
	b[i].place(x=x[i], y=y[i])
entries = {'placeholder1': e[0].get(), 'placeholder2': e[1].get()}

with open('need\\temp', 'wb') as f:
	f.write(str(entries).encode())
