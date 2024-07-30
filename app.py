import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
from PIL import Image, ImageTk
import time
import datetime
import configparser

class Timelog:
    def __init__(self):
        self.version = 'v1'

        self.timer_on = 0

        self.start_time = 0
        self.elapsed_time = 0
        self.total_elapsed_time = 0
        self.last_saved_time = 0

        self.root = tk.Tk(className='timelogtk')
        self.root.geometry('340x490')
        self.root.resizable(False, False)
        self.root.title('Timelog ' + self.version)
        self.root.configure(background='white')

        self.frame_style = Style()
        self.frame_style.configure('timelog.TFrame', background='white')

        self.frame = ttk.Frame(self.root, padding=10, style='timelog.TFrame')
        self.frame.grid()
        self.frame.pack(anchor='center')

        self.logo = Image.open('logo.png')
        self.logo = self.logo.resize((50,50))
        self.logo_photo = ImageTk.PhotoImage(self.logo)
        self.logo_label = ttk.Label(self.frame, image=self.logo_photo)
        self.logo_label.grid(column=0, row=0, pady=(60,0))

        self.time_label = ttk.Label(self.frame, font=('calibri', 45), background='white')
        self.time_label.grid(column=0, row=1, pady=(60,0))
        self.time_label.config(text=time.strftime('%H:%M:%S',time.gmtime(self.start_time)))

        self.start_button = ttk.Button(self.frame, text='Start', command=self.handler_start_button_press, width=18)
        self.start_button.grid(column=0, row=2, pady=(15,0))

        self.save_button = ttk.Button(self.frame, text='Save', command=self.handler_save_button_press)
        self.save_button.grid(column=0, row=3, pady=(70,0))
        self.save_button['state'] = tk.DISABLED

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.file = config.get('File', 'Location')
        self.file_lines = []

    def update_time(self):
        if self.timer_on == 0:
            return;
        self.save_button['state'] = tk.NORMAL
        self.elapsed_time = time.time() - self.start_time
        self.time_label.config(text=time.strftime('%H:%M:%S', time.gmtime(self.total_elapsed_time + self.elapsed_time)))
        self.time_label.after(1000, self.update_time)

    def handler_start_button_press(self):
        if self.start_button['text'] == 'Start':
            # Start button pressed
            self.timer_on = 1
            self.start_button['text'] = 'Stop'
            self.start_time = time.time()
            self.update_time()
        else:
            # Stop button pressed
            self.timer_on = 0
            self.start_button['text'] = 'Start'
            self.total_elapsed_time += self.elapsed_time

    def handler_save_button_press(self):
        self.save_button['state'] = tk.DISABLED
        time_diff = self.total_elapsed_time - self.last_saved_time # time to add to file
        self.save_file(time_diff)
        self.last_saved_time = self.total_elapsed_time

    def save_file(self, seconds_to_add):
        with open(self.file) as f:
            for line in f:
                self.file_lines.append(line)

        parts = self.file_lines[-1].split(',')
        date_part = parts[0]
        time_part = parts[1].strip()

        file_dt = datetime.datetime.strptime(date_part, "%m/%d/%Y")
        now_dt = datetime.datetime.now()

        if file_dt.date() == now_dt.date():
            # modify last line, overwrite file
            entry = []
            entry.append(now_dt.strftime('%m/%d/%Y'))
            time_part_parts = time_part.split(':')
            time_part_in_seconds = datetime.timedelta(hours=int(time_part_parts[0]), minutes=int(time_part_parts[1]), seconds=int(time_part_parts[2]))
            entry.append(time.strftime('%H:%M:%S', time.gmtime(seconds_to_add + time_part_in_seconds.total_seconds())))
            self.file_lines[-1] = entry[0] + ", " + entry[1] + "\n"

            with open(self.file, 'a') as f:
                for line in self.file_lines:
                    f.write(line)
        else:
            # append new line to end of file
            entry = []
            entry.append(now_dt.strftime('%m/%d/%Y'))
            entry.append(time.strftime('%H:%M:%S',time.gmtime(seconds_to_add)))
            self.file_lines.append(entry[0] + ", " + entry[1] + "\n")

            with open(self.file, 'a') as f:
                f.write(self.file_lines[-1])

    def Start(self):
        self.root.mainloop()

timelog = Timelog()
timelog.Start()