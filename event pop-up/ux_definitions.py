from initials import *

buttons = {}


def b_ok():
	global buttons

	with open('need\\temp', 'rb') as f:
		print(eval(f.readline().decode())['placeholder1'])

	root.destroy()

	buttons['OK'] = True
	return 'OK'


def b_cancel():
	global buttons

	root.destroy()

	buttons['Cancel'] = True
	return 'Cancel'
