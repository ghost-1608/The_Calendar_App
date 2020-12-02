#CS Project - Calander

import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
MONTHS = [
	'January', 'February', 'March', 'April', 'May', 'June', 'July',
	'August', 'September', 'October', 'November', 'December',
]
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TODAY = dt.datetime.today()


def day_of_week(year, month, day):
	t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
	year -= month < 3
	return (year + int(year/4) - int(year/100) + int(year/400) + t[month-1] + day) % 7


def is_leap(year):
	if year % 100:
		return not(year % 4)
	else:
		return not(year % 400)


class Date:
	def __init__(self, yyyy, mm, dd):
		self.dd = dd
		self.mm = mm
		self.yyyy = yyyy
		self.day = day_of_week(yyyy, mm, dd)

	def next_month(self):
		mm = self.mm + 1
		yyyy = self.yyyy
		if mm > 12:
			mm = 1
			yyyy += 1
		return Date(yyyy, mm, self.dd)

	def prev_month(self):
		mm = self.mm - 1
		yyyy = self.yyyy
		if mm < 1:
			mm = 12
			yyyy -= 1
		return Date(yyyy, mm, self.dd)


def create_calender(date):
	yyyy = date.yyyy
	mm = date.mm
	dd = date.dd

	frame = tk.Frame(main_frame)
	week_frames = [tk.Frame(frame) for i in range(7)]

	if is_leap(yyyy):
		DAYS_IN_MONTH[1] = 29
	else:
		DAYS_IN_MONTH[1] = 28

	for day in DAYS:
		tk.Label(week_frames[0], text=day[:3], width=3).pack(side='left', expand=True, fill='both', anchor='center')
	month_no = 0
	day_no = 0
	first_day = day_of_week(yyyy, mm, 1)
	for week in range(6):
		for day in range(7):
			if day_no == 0:
				if day == first_day:
					disp = '1'
					day_no = 1
					month_no = 1
					state = 'normal'
				else:
					disp = str(DAYS_IN_MONTH[mm-1]-(first_day-day)+1)
					state = 'disabled'
			else:
				if day_no < DAYS_IN_MONTH[mm-1]:
					day_no += 1
				else:
					month_no = 2
					day_no = 1
					state = 'disabled'
				disp = str(day_no)

			if dd == day_no and month_no == 1:
				tk.Button(week_frames[week+1], text=disp, state=state, bg='#48D', fg='white', font=('Courier', 12), width=3, height=1).pack(side='left', expand=True, fill='both')
				continue
			ttk.Button(week_frames[week+1], text=disp, state=state, style='Calender.TButton').pack(side='left', expand=True, fill='both')
			

	for i in range(len(week_frames)):
		week_frames[i].pack(fill='both', expand=True)

	return frame


def preload_calender():
	global calender_frames
	calender_frames[-1] = create_calender(view.prev_month())
	calender_frames[1] = create_calender(view.next_month())


def switch_month(value):	
	global calender_frames, view
	calender_frames[0].pack_forget()
	if value == 1:
		view = view.next_month()
		calender_frames[1].pack(fill='both', expand=True)
		calender_frames[0] = calender_frames[1]
	else:
		view = view.prev_month()
		calender_frames[-1].pack(fill='both', expand=True)
		calender_frames[0] = calender_frames[-1]
	month_label.config(text=MONTHS[view.mm-1]+', '+str(view.yyyy))
	preload_calender()



def keypressed(event):	
	if event.char == 'q' or event.keycode == 37:
		switch_month(-1)
	if event.char == 'e' or event.keycode == 39:
		switch_month(1)


view = Date(TODAY.year, TODAY.month, TODAY.day)
calender_frames = {-1:None, 0:None, 1:None}

root = tk.Tk()
root.title('Calender')
root.bind('<KeyRelease>', keypressed)
main_frame = tk.Frame(root)

style = ttk.Style()
style.configure('Calender.TButton', font=('Courier', 12), width=3, height=1)

month_frame = tk.Frame(main_frame, height=1)
month_label = tk.Label(month_frame, text=MONTHS[view.mm-1]+', '+str(view.yyyy), font=('', 16))
nav_frame = tk.Frame(month_frame, height=1)
left_month_btn = tk.Button(nav_frame, text='<', command=lambda: switch_month(-1))
right_month_btn = tk.Button(nav_frame, text='>', command=lambda: switch_month(1))

month_label.pack(side='left', padx=(3, 10), pady=(5, 1))
left_month_btn.pack(side='left')
right_month_btn.pack(side='right')
nav_frame.pack(side='right')
month_frame.pack(side='top', fill='x', expand=True)

calender_frames[0] = create_calender(view)
calender_frames[0].pack(fill='both', expand=True)
preload_calender()

main_frame.pack(expand=True, fill='both')

'''
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Server Info", state='disabled')
filemenu.add_command(label="Join New", state='disabled')
filemenu.add_command(label="Host New", state='disabled')
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="Main", menu=filemenu)

settingsmenu = tk.Menu(menubar, tearoff=0)
settingsmenu.add_command(label='Clear Screen')
settingsmenu.add_command(label='Toggle Dark Mode')
menubar.add_cascade(label="Options", menu=settingsmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)
'''
while True:
	try:
		root.update()
	except:
		exit(0)
