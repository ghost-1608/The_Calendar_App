#CS Project - Calender

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext
import datetime as dt
from time import strftime
from functools import partial
import os
import pickle
import requests

DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December',
]
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TODAY = dt.datetime.today()


def day_of_week(year, month, day):
    '''Returns the day of the week for the specified date'''
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    year -= month < 3
    return (year + int(year/4) - int(year/100) + int(year/400) + t[month-1] + day) % 7


def is_leap(year):
    '''Check if given year is a leap year or not'''
    if year % 100:
        return not(year % 4)
    else:
        return not(year % 400)


class Date:
    '''A class for storing and manipulation of Calender Dates'''
    def __init__(self, yyyy, mm, dd):
        self.dd = dd
        self.mm = mm
        self.yyyy = yyyy
        self.day = day_of_week(yyyy, mm, dd)

    def __str__(self):
        return str(self.yyyy) + '-' + str(self.mm) + '-' + str(self.dd)

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
    '''Returns a frame containing all the days of a month for the given date'''

    #Extracting values from the date datatype
    yyyy = date.yyyy
    mm = date.mm
    dd = date.dd

    #Creating the required frames
    frame = tk.Frame(main_frame)                       #The main frame which shall be returned
    week_frames = [tk.Frame(frame) for i in range(7)]  #Frame containing 6 rows for weeks + 1 row for days

    #Updating DAYS_IN_MONTH for the given year
    if is_leap(yyyy):
        DAYS_IN_MONTH[1] = 29
    else:
        DAYS_IN_MONTH[1] = 28

    #Adding day field to the first frame of week_frames
    for day in DAYS: 
        tk.Label(week_frames[0], text=day[:3], width=3).pack(side='left', expand=True, fill='both', anchor='center')

    month_no = 0 #iterating month (0 for previous month, 1 for current month, 2 for next month)
    day_no = 0   #iterating day
    first_day = day_of_week(yyyy, mm, 1) #finding out from which day does the month start

    #Looping through all days in the calender for the given month
    for week in range(6):
        for day in range(7):
            if day_no == 0:
                if day == first_day:
                    disp = '1'
                    day_no = 1
                    month_no = 1
                    state = 'normal'
                else:
                    disp = str(DAYS_IN_MONTH[mm-2]-(first_day-day)+1)
                    state = 'disabled'
            else:
                if day_no < DAYS_IN_MONTH[mm-1]:
                    day_no += 1
                else:
                    month_no = 2
                    day_no = 1
                    state = 'disabled'
                disp = str(day_no)

            if dd == day_no and month_no == 1 and mm == TODAY.month and yyyy == TODAY.year:
                if has_event((yyyy, mm, day_no)):
                    tk.Button(week_frames[week+1], text=disp, state=state, bg='#48D', fg='white', font=('Courier', 12, 'underline'), width=3, height=1, command=partial(set_date_selected, yyyy, mm, day_no)).pack(side='left', expand=True, fill='both')
                else:
                    tk.Button(week_frames[week+1], text=disp, state=state, bg='#48D', fg='white', font=('Courier', 12), width=3, height=1, command=partial(set_date_selected, yyyy, mm, day_no)).pack(side='left', expand=True, fill='both')
                continue
            if has_event((yyyy, mm, day_no)):
                ttk.Button(week_frames[week+1], text=disp, state=state, style='CalenderEvent.TButton', command=partial(set_date_selected, yyyy, mm, day_no)).pack(side='left', expand=True, fill='both')
            else:
                ttk.Button(week_frames[week+1], text=disp, state=state, style='Calender.TButton', command=partial(set_date_selected, yyyy, mm, day_no)).pack(side='left', expand=True, fill='both')
            

    for i in range(len(week_frames)):
        week_frames[i].pack(fill='both', expand=True)

    return frame


def has_event(date):
    for e in events.keys():
        if e[2] == date[2]:
            if e[1] == date[1]:
                for i in events[e]:
                    if i[2] == 'Yearly':
                        return True
            else: 
                for i in events[e]:
                    if i[2] == 'Monthly':
                        return True
    return bool(events.get(date, False))


def preload_calender():
    '''Preload the calender frame for the preceding and the successive month'''
    global calender_frames
    calender_frames[-1] = create_calender(view.prev_month())
    calender_frames[1] = create_calender(view.next_month())


def switch_month(value):
    '''Switch month by value; +1 for next month, -1 for previous month, 0 for refresh'''
    global calender_frames, view    
    calender_frames[0].pack_forget()
    if value == 1:
        view = view.next_month()
        calender_frames[1].pack(fill='both', expand=True)
        calender_frames[0] = calender_frames[1]
    elif value == -1:
        view = view.prev_month()
        calender_frames[-1].pack(fill='both', expand=True)
        calender_frames[0] = calender_frames[-1]
    else:
        calender_frames[0] = create_calender(view)
        calender_frames[0].pack(fill='both', expand=True)
    month_label.config(text=MONTHS[view.mm-1]+', '+str(view.yyyy))
    preload_calender()



def set_date_selected(yyyy, mm, dd):
    global date_selected
    date_selected = Date(yyyy, mm, dd)
    event_tree.heading('#0', text='Events on '+str(date_selected))
    display_events()


def keypressed(event):
    '''Called when any key is pressed'''
    if event.char == 'q' or event.keycode == 37:
        switch_month(-1)
    if event.char == 'e' or event.keycode == 39:
        switch_month(1)


def update_time():
    '''Updating the time'''
    global TODAY, view
    t = strftime('%H:%M:%S%p')
    if t[3:8] == '00:00':
        try:
            TODAY = dt.datetime.today()
            view = Date(TODAY.year, TODAY.month, TODAY.day)
            switch_month(0)
        except:
            pass
    label_t['text'] = t
    label_t.after(1000, update_time)


def display_events():
    yyyy = date_selected.yyyy
    mm = date_selected.mm
    dd = date_selected.dd

    event_tree.delete(*event_tree.get_children())
    for e in events.keys():
        if e[2] == dd:
            if e[1] == mm:
                for i in range(len(events[e])):
                    if events[e][i][2] == 'Yearly':
                        event_tree.insert('', index='end', text=events[e][i][0], value=(str(e), i, str(events[e][i])))
                    elif e[0] == yyyy:
                        event_tree.insert('', index='end', text=events[e][i][0], value=(str(e), i, str(events[e][i])))
            else: 
                for i in range(len(events[e])):
                    if events[e][i][2] == 'Monthly':
                        event_tree.insert('', index='end', text=events[e][i][0], value=(str(e), i, str(events[e][i])))



def delete_event(date, index, window):
    global events
    try:
        events[date].pop(index)
        if not events[date]:
            del events[date]
        with open('storage.bin', 'wb') as file:
            pickle.dump(events, file)
        switch_month(0)
        window.destroy()
    except:
        pass


def event_select(event=None):
    value = event_tree.item(event_tree.selection()[0], 'value')
    popup = tk.Toplevel(root)
    popup.title(eval(value[-1])[0])
    popup.minsize(300, 200)
    tk.Label(popup, text=eval(value[-1])[0] + ' (' + str(date_selected) + ')', font=('Courier', 14, 'bold')).pack(side='top', fill='x')
    tk.Message(popup, text=eval(value[-1])[-1], font=('Courier', 12)).pack()
    tk.Button(popup, text='Delete Event', bg='#F21', fg='#FFF', font=('Courier', 12), command=lambda: delete_event(eval(value[0]), eval(value[1]), popup)).pack()


def weather():
    B=100
    L=500
    CITY='chennai'
    '''
    {
    'coord': {'lon': 78.47, 'lat': 17.38}, 
    'weather': [{'id': 721, 'main': 'Haze', 'description': 'haze', 'icon': '50n'}], 
    'base': 'stations',
    'main': {'temp': 23.67, 'feels_like': 25.1, 'temp_min': 23, 'temp_max': 24, 'pressure': 1016, 'humidity': 60}, 
    'visibility': 5000, 
    'wind': {'speed': 0.5, 'deg': 0},
    'clouds': {'all': 13},
    'dt': 1606827794,
    'sys': {'type': 1, 'id': 9214,
    'country': 'IN',
    'sunrise': 1606784427,
    'sunset': 1606824621},
    'timezone': 19800,
    'id': 1269843,
    'name': 'Hyderabad',
    'cod': 200
    }
    '''

    #api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
    #d1f00b521eb58c2a2721dfefacc66c3a


    def change(window, city):
        window.title('Change city (current: '+city+')')
        get_weather(city.lower())

    def city_select():
        win=tk.Toplevel()
        win.title('Change city (current: '+CITY+')')
        win.geometry('500x100')

        entry=tk.Entry(win)
        entry.place(relx=0.1,rely=0.4,relwidth=0.7,relheight=0.2)

        confirm=tk.Button(win,text='confirm',command=lambda:change(win, entry.get()))
        confirm.place(relx=0.8,rely=0.4,relwidth=0.2,relheight=0.2)

        win.mainloop()

    def get_weather(city):
        global CITY
        CITY = city
        appid='d1f00b521eb58c2a2721dfefacc66c3a'
        url='https://api.openweathermap.org/data/2.5/weather'
        parameters = {'appid':appid,'q':city, 'units':'metric'}
        response=requests.get(url, params=parameters)
        response=response.json()
        label_w['text']=str(response['weather'][0]['description'])+'\n'+'temp:'+str(response['main']['temp'])+'\n'+'feels like:'+str(response['main']['feels_like'])
    
    win=tk.Toplevel()
    win.title("Weather today")
    win.geometry(str(L)+'x'+str(B))

    canvas=tk.Canvas(win,width=500,height=500, bg='#EEEDE7')
    canvas.pack()

    weather=tk.Frame(win,bg='#CBCDCB')
    weather.place(relx=0.02,rely=0.02,relheight=0.96,relwidth=0.96)

    label_w=tk.Label(weather,font=('lucida console',20,"bold"),fg="#607D86",bg='#CBCDCB')
    label_w.place(relheight=1,relwidth=1)

    select_city=tk.Button(label_w,text='select city',command=lambda:city_select())
    select_city.place(relx=0.8,rely=0.8,relwidth=0.2,relheight=0.2)
    get_weather(CITY)
    win.mainloop()

    

def generate_event_ui():
    ''' This is kinda complex lol'''
    def on_b_ok():
        global events
        responses = []

        for i in e:
            responses += [i.get()]

        for i in C:
            for j in i:
                responses += [j.get()]

        for i in o:
            if i.get() == 'None':
                responses += ['None']
            else:
                responses += [eval(i.get())[0]]

        for i in m:
            responses += [i.get('1.0', 'end-1c')]

        try:
            yyyy = int(responses[4])
            mm = MONTHS.index(responses[3]) + 1
            dd = int(responses[2])
        except:
            popup.destroy()
            return

        if has_event((yyyy, mm, dd)):
            events[(yyyy, mm, dd)].append([responses[0], responses[1], responses[5], responses[6]])
        else:
            events[(yyyy, mm, dd)] = [[responses[0], responses[1], responses[5], responses[6]]]

        with open('storage.bin', 'wb') as file:
            pickle.dump(events, file)

        switch_month(0)
        popup.destroy()


    def on_b_cancel():
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title('Add event')
    popup.resizable(False, False)
    canvas = tk.Canvas(popup, width=540, height=480, highlightthickness=False)
    l, e, c, C, d, o, m = [], [], [], [], [], [], []
    b_x, b_y = 100, 40
    X, Y = 10, 50

    event_name = {'label': tk.Label(canvas, text='Event Name: '), 'entry': tk.Entry(canvas)}
    l += [event_name['label']]
    e += [event_name['entry']]

    tags = {'label': tk.Label(canvas, text='Tags: '), 'entry': tk.Entry(canvas)}
    l += [tags['label']]
    e += [tags['entry']]

    days = [str(i) for i in range(1, 32)]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = [str(i) for i in range(1900, 2101)]
    n = [tk.StringVar() for i in range(3)]
    date = {'label': tk.Label(canvas, text='Dates: '),
            'value': [ttk.Combobox(canvas, state='readonly', width=2, textvariable=n[0]),
                      ttk.Combobox(canvas, state='readonly', width=10, textvariable=n[1]),
                      ttk.Combobox(canvas, state='readonly', width=4, textvariable=n[2])]}
    date['value'][0]['values'] = days
    date['value'][1]['values'] = months
    date['value'][2]['values'] = years
    l += [date['label']]
    c += [date['value']]
    C += [n]

    v = tk.StringVar(canvas)
    v.set('None')
    repeat_select = {'label': tk.Label(canvas, text='Repeat: '),
                     'value': tk.OptionMenu(canvas, v, ['None'], ['Monthly'], ['Yearly'])} # ['Daily'], ['Weekly'], 
    repeat_select['value'].configure(takefocus=True)
    
    l += [repeat_select['label']]
    d += [repeat_select['value']]
    o += [v]

    multi_textbox = {'label': tk.Label(canvas, text='Description: '),
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
        tk.Label(canvas, text='DD:').place(x=x, y=y)
        i[0].place(x=x + 35, y=y)
        tk.Label(canvas, text='M:').place(x=x + 90, y=y)
        i[1].place(x=x + 120, y=y)
        tk.Label(canvas, text='YYYY:').place(x=x + 220, y=y)
        i[2].place(x=x + 270, y=y)
        y += b_y

    for i in d:
        i.place(x=x - 2, y=y - 5)
        y += b_y

    for i in m:
        i.place(x=x, y=y + 2)
        y += b_y

    b_ok = tk.Button(canvas, text='OK', command=on_b_ok)
    b_cancel = tk.Button(canvas, text='Cancel', command=on_b_cancel)

    b_ok.place(x=420, y=450)
    b_cancel.place(x=470, y=450)

    canvas.pack()


def about():
    popup = tk.Toplevel(root)
    popup.title('About')
    text = r"""

   ______      __               __             ___              
  / ____/___ _/ /__  ____  ____/ /__  _____   /   |  ____  ____ 
 / /   / __ `/ / _ \/ __ \/ __  / _ \/ ___/  / /| | / __ \/ __ \
/ /___/ /_/ / /  __/ / / / /_/ /  __/ /     / ___ |/ /_/ / /_/ /
\____/\__,_/_/\___/_/ /_/\__,_/\___/_/     /_/  |_/ .___/ .___/
                                                 /_/   /_/      
    Calender App v1.00 Beta
    An all in one calender + time + weather application

    +----------------------------------+
    |    Created by,                   |
    |    ~ Arka 'Ghost' Ghosh          |
    |    ~ Kavirajar 'Data Overflow'   |
    |    ~ Lohith Sarathy              |
    +----------------------------------+

    """
    tk.Label(popup, text=text, font = ('Courier New','12')).pack()
    
view = Date(TODAY.year, TODAY.month, TODAY.day)
calender_frames = {-1:None, 0:None, 1:None}
date_selected = Date(TODAY.year, TODAY.month, TODAY.day)

events = {}
# Structure for events is
# {
#     (yyyy, mm, dd):[ [event_name, tags, occurance, description], [<event2>], [<event3>], [<eventn>] ],
#     (<some other date>): [ <same as above> ],
# }
if os.path.exists('storage.bin') and os.path.getsize('storage.bin'):
    with open('storage.bin', 'rb') as file:
        events = pickle.load(file)

#Creating the Graphical User Interface
root = tk.Tk()
root.minsize(480, 330)
root.title('Calender')
root.bind('<KeyRelease>', keypressed)
main_frame = tk.Frame(root)

style = ttk.Style()
style.configure('Calender.TButton', font=('Courier', 12), width=3, height=1)
style.configure('CalenderEvent.TButton', font=('Courier', 12, 'underline'), width=3, height=1)
style.configure('Treeview.Heading', font=(None, 10, 'bold'))

#Setting up the time UI
time_frame = tk.Frame(main_frame)
label_t = tk.Label(time_frame, font=('lucida console', 24, "bold"), fg="#607D86", bg='#CBCDCB')
update_time()

#Setting up the month and navigation UI
month_frame = tk.Frame(main_frame, height=1)
month_label = tk.Label(month_frame, text=MONTHS[view.mm-1]+', '+str(view.yyyy), font=('', 16))
nav_frame = tk.Frame(month_frame, height=1)
left_month_btn = tk.Button(nav_frame, text='<', command=lambda: switch_month(-1))
right_month_btn = tk.Button(nav_frame, text='>', command=lambda: switch_month(1))

#Setting up the event system and UI (popup)
event_frame = tk.Frame(main_frame)
event_tree = ttk.Treeview(event_frame)
event_tree.bind("<<TreeviewSelect>>", event_select)
event_tree.heading('#0', text='Events on '+str(date_selected))
event_tree.column("#0", minwidth=10)
add_event_btn = tk.Button(event_frame, text='Add Event', command=generate_event_ui)
add_event_btn.pack(side='bottom')
event_tree.pack(expand=True, fill='y')

#Setting up the menu
menubar = tk.Menu(root)
mainmenu = tk.Menu(menubar, tearoff=0)
mainmenu.add_command(label="Refresh", command=lambda: switch_month(0))
mainmenu.add_command(label="Next Month", command=lambda: switch_month(1))
mainmenu.add_command(label="Previous Month", command=lambda: switch_month(-1))
mainmenu.add_command(label="Weather Today", command=weather)
mainmenu.add_separator()
mainmenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="Main", menu=mainmenu)

eventmenu = tk.Menu(menubar, tearoff=0)
eventmenu.add_command(label="Add Event", command=generate_event_ui)
menubar.add_cascade(label="Event", menu=eventmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

#Packing them all up
label_t.pack()
time_frame.pack(side='top')
month_label.pack(side='left', padx=(3, 10), pady=(5, 1))
left_month_btn.pack(side='left')
right_month_btn.pack(side='right')
nav_frame.pack(side='right')
month_frame.pack(side='top', fill='x')
event_frame.pack(side='right', fill='y')

#Creating the calender
calender_frames[0] = create_calender(view)
calender_frames[0].pack(fill='both', expand=True)
preload_calender()

#Pack the mainframe and start the main loop
main_frame.pack(expand=True, fill='both')
root.mainloop()

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

while True:
    try:
        root.update()
    except:
        break
'''