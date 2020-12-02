from initials import *
from ui_definitions import *
from ux_definitions import *

b_ok = tkinter.Button(canvas, text='OK', command=b_ok)
b_cancel = tkinter.Button(canvas, text='Cancel', command=b_cancel)

b_ok.place(x=width - 120, y=height - 30)
b_cancel.place(x=width - 70, y=height - 30)

canvas.pack()
root.mainloop()
