import tkinter as tk
from tkinter import ttk
from time import strftime
from tkinter.ttk import Style
from PIL import Image, ImageTk

def time():
    system_time = strftime('%H:%M:%S')
    time_label.config(text=system_time)
    time_label.after(1000, time)

def start_button_press():
    print(start_button['text'])
    start_button['text'] = 'Start' if start_button['text'] == 'Stop' else 'Stop'
    save_button['state'] = tk.NORMAL

def save_button_press():
    save_button['state'] = tk.DISABLED
    print("SAVE")

version = 'v1'

root = tk.Tk(className='timelogtk')
root.geometry('340x490')
root.resizable(False, False)
root.title('Timelog ' + version)
root.configure(background='white')

frame_style = Style()
frame_style.configure('timelog.TFrame', background='white')

frame = ttk.Frame(root, padding=10, style='timelog.TFrame')
frame.grid()
frame.pack(anchor='center')

logo = Image.open('logo.png')
logo = logo.resize((50,50))
logo_photo = ImageTk.PhotoImage(logo)
logo_label = ttk.Label(frame, image=logo_photo)
logo_label.grid(column=0, row=0, pady=(60,0))

time_label = ttk.Label(frame, font=('calibri', 45), background='white')
time_label.grid(column=0, row=1, pady=(60,0))

start_button = ttk.Button(frame, text='Start', command=start_button_press, width=18)
start_button.grid(column=0, row=2, pady=(15,0))

save_button = ttk.Button(frame, text='Save', command=save_button_press)
save_button.grid(column=0, row=3, pady=(70,0))
save_button['state'] = tk.DISABLED

time()

root.mainloop()