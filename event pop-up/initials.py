import tkinter

with open('config.ini') as f:
    de = eval(f.read())

bg = '#d5d5d5'

root = tkinter.Tk()
root.geometry(str(de['width']) + 'x' + str(de['height']))
canvas = tkinter.Canvas(root, width=de['width'], height=de['height'])

width, height = de['width'], de['height']

root.resizable(False, False)
