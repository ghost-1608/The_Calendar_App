from initials import *
from ui_definitions import *
import ux_definitions

b_ok = tkinter.Button(canvas, text='OK', command=ux_definitions.b_ok)
b_cancel = tkinter.Button(canvas, text='Cancel', command=ux_definitions.b_cancel)

b_ok.place(x=width - 120, y=height - 30)
b_cancel.place(x=width - 70, y=height - 30)

root.bind('<Return>', ux_definitions.b_ok)

canvas.pack()
root.mainloop()
