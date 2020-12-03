import tkinter as tk
from time import strftime

B=100
L=500

def update_time():
    t=strftime('%H:%M:%S%p')
    label_t['text']=t
    label_t.after(1000,update_time)


#grey: #EEEDE7
#light grey: #CBCDCB
#blueish grey: #607D86
win=tk.Tk(screenName="Weather today")
win.geometry(str(L)+'x'+str(B))

canvas=tk.Canvas(win,width=500,height=500, bg='#EEEDE7')
canvas.pack()

time=tk.Frame(win,bg='#CBCDCB')
time.place(relx=0.02,rely=0.02,relheight=0.96,relwidth=0.96)

label_t=tk.Label(time,font=('lucida console',55,"bold"),fg="#607D86",bg='#CBCDCB')
label_t.pack()
update_time()

win.mainloop()
