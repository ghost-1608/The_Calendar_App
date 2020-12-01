c = False

with open('config.ini') as f:
    d = f.read()

try:
    d = eval(d)
    if 'dict' not in str(type(d)):
        c = True
except:
    c = True

if c:
    print('Configuration file corrupted!')
else:
    b_x, b_y = 100, 30

    if 'buffer_x' in d.keys():
        b_x = d['buffer_x']
    if 'buffer_y' in d.keys():
        b_y = d['buffer_y']

    with open('initials.py', 'w') as f:
        f.write('import tkinter\n\n')
        f.write('root = tkinter.Tk()\n')
        f.write("root.geometry('" + str(d['width']) + 'x' + str(d['height']) + "') \n\n")
        f.write("with open('need\\\\temp', 'wb'):\n")
        f.write('\tpass\n\n')

        if 'title' in d.keys():
            f.write("root.title('" + d['title'] + "')\n")

    with open('ui_definitions.py', 'w') as f:
        f.write('from ux_definitions import *\n\n')

        f.write('l = [')
        for i in range(len(d['labeled_entries'])):
            f.write("tkinter.Label(root, text='" + d['labeled_entries'][i] + "')")
            if i != len(d['labeled_entries']) - 1:
                f.write(', ')
        f.write(']\n')

        f.write('e = [')
        for j in range(len(d['labeled_entries'])):
            f.write('tkinter.Entry(root)')
            if j != len(d['labeled_entries']) - 1:
                f.write(', ')
        f.write(']\n\n')

        x, y = d['x'], d['y']

        f.write('y = ' + str(y) + '\n\n')

        f.write('for i in l:\n')
        f.write('\ti.place(x=' + str(x) + ', y=y)\n')
        f.write('\ty += ' + str(b_y) + '\n\n')

        x, y = d['x'] + b_x, d['y']

        f.write('y = ' + str(y) + '\n\n')

        f.write('for i in e:\n')
        f.write('\ti.place(x=' + str(x) + ', y=y)\n')
        f.write('\ty += ' + str(b_y) + '\n\n')

        btn = [{'label': 'OK', 'x': d['width'] - 120, 'y': d['height'] - 50, 'command': 'b_ok'}, {'label': 'Cancel', 'x': d['width'] - 80, 'y': d['height'] - 50, 'command': 'b_cancel'}]

        if 'buttons' in d.keys():
            btn = d['buttons']

        f.write('b = [')
        for a in range(len(btn)):
            f.write("tkinter.Button(root, text='" + btn[a]['label'] + "', command=" + btn[a]['command'] + ')')
            if a != len(btn) - 1:
                f.write(', ')
        f.write(']\n\n')

        f.write('x, y = ' + str([i['x'] for i in btn]) + ', ' + str([i['y'] for i in btn]) + '\n\n')

        f.write('for i in range(len(b)):\n')
        f.write('\tb[i].place(x=x[i], y=y[i])\n')

        f.write('entries = {')

        for a in range(len(d['labeled_entries'])):
            f.write("'" + d['labeled_entries'][a] + "': e[" + str(a) + '].get()')
            if a != len(d['labeled_entries']) - 1:
                f.write(', ')
        f.write('}\n\n')

        f.write("with open('need\\\\temp', 'wb') as f:\n")
        f.write("\tf.write(str(entries).encode())\n\n")
