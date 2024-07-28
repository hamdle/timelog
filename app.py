from tkinter import *
from tkinter import ttk
from time import strftime

root = Tk()
root.geometry('350x500')
root.resizable(False, False)
root.title('Timelog')

def time():
    system_time = strftime('%H:%M:%S')
    label.config(text=system_time)
    label.after(1000, time)

label = Label(root, font=('calibri', 40, 'bold'))
label.pack(anchor='center')

time()
 
root.mainloop()