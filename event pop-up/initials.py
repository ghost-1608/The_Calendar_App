import tkinter

with open('config.ini') as f:
    d = eval(f.read())

root = tkinter.Tk()
root.geometry(str(d['width']) + 'x' + str(d['height']))
canvas = tkinter.Canvas(root, width=d['width'], height=d['height'])

width, height = d['width'], d['height']
