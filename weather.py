import tkinter as tk
import requests

#CBCDCB
#blueish grey: #607D86

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


def change(city):
    get_weather(city.lower())

def city_select():
    win=tk.Tk(screenName='select city')
    win.geometry('500x100')

    entry=tk.Entry(win)
    entry.place(relx=0.1,rely=0.4,relwidth=0.7,relheight=0.2)

    confirm=tk.Button(win,text='confirm',command=lambda:change(entry.get()))
    confirm.place(relx=0.8,rely=0.4,relwidth=0.2,relheight=0.2)

    win.mainloop()

def get_weather(city):
    appid='d1f00b521eb58c2a2721dfefacc66c3a'
    url='https://api.openweathermap.org/data/2.5/weather'
    parameters = {'appid':appid,'q':city, 'units':'metric'}
    response=requests.get(url, params=parameters)
    response=response.json()
    label_w['text']=str(response['weather'][0]['description'])+'\n'+'temp:'+str(response['main']['temp'])+'\n'+'feels like:'+str(response['main']['feels_like'])
    
    


win=tk.Tk(screenName="Weather today")
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
