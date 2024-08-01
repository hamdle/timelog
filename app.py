import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
from PIL import Image, ImageTk
import time
import datetime
import configparser
from tkinter.messagebox import askyesno

class Timelog:
    def __init__(self):
        self.version = '1.0'

        self.timer_on = False
        self.elapsed_time = 0           # elapsed time since Start button pressed
        self.total_elapsed_time = 0     # total elapsed time of all Start/Stop cycles
        self.last_saved_time = 0


        self.root = tk.Tk(className='timelogtk')
        self.root.geometry('300x430')
        self.root.resizable(False, False)
        self.root.title('Timelog')
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
        self.logo_label.grid(column=0, row=0, pady=(40,0))

        self.time_label = ttk.Label(self.frame, font=('Arial', 38), background='white')
        self.time_label.grid(column=0, row=1, pady=(40,0))
        self.time_label.config(text=time.strftime('%H:%M:%S',time.gmtime(0)))

        self.start_button = ttk.Button(self.frame, text='Start', command=self.handler_start_button_press, width=12)
        self.start_button.grid(column=0, row=2, pady=(12,0))

        self.saved_time_label = ttk.Label(self.frame, font=('Arial', 24), background='white', foreground='#0ac50a')
        self.saved_time_label.grid(column=0, row=3, pady=(20, 0))
        self.saved_time_label.config(text="")

        self.save_button = ttk.Button(self.frame, text='Save', command=self.handler_save_button_press)
        self.save_button.grid(column=0, row=4, pady=(16,0), padx=(0,0))
        # self.save_button.grid(column=0, row=4, pady=(27,0), padx=(30,0))
        self.save_button['state'] = tk.DISABLED

        self.upload = Image.open('upload.png')
        self.upload = self.upload.resize((19, 19))
        self.upload_image = ImageTk.PhotoImage(self.upload)
        self.upload_button = ttk.Button(self.frame, image=self.upload_image, command=self.handler_confirm_upload)
        self.upload_button.grid(column=0, row=5, pady=(22, 0), padx=(0,0))
        #self.upload_button['state'] = tk.DISABLED
        self.upload_in_progress = 0

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.file = config.get('File', 'Location')
        self.file_lines = []

        self.root.tk.call('tk', 'scaling', 1.0)

    def update_time(self, wait = False):
        if self.timer_on == False:
            return;
        if str(self.save_button['state']) == tk.DISABLED:
            self.save_button['state'] = tk.NORMAL
        if wait == False:
            self.elapsed_time += 1
        self.time_label.config(text=time.strftime('%H:%M:%S', time.gmtime(self.total_elapsed_time + self.elapsed_time)))
        self.time_label.after(1000, self.update_time)

    def handler_start_button_press(self):
        if self.start_button['text'] == 'Start':
            # Start button pressed
            self.timer_on = True
            self.start_button['text'] = 'Pause'
            self.update_time(True)
        else:
            # Stop button pressed
            self.timer_on = False
            self.start_button['text'] = 'Start'
            self.total_elapsed_time += self.elapsed_time
            self.elapsed_time = 0

    def handler_save_button_press(self):
        self.save_button['state'] = tk.DISABLED
        if self.timer_on == True:
            self.total_elapsed_time += self.elapsed_time
        self.save_file(self.total_elapsed_time - self.last_saved_time)
        self.elapsed_time = 0
        self.last_saved_time = self.total_elapsed_time

    def handler_confirm_upload(self):
        answer = askyesno(title='Confirm', message='Upload timesheet?')
        if answer:
            self.handler_upload_button_press()

    def handler_upload_button_press(self):
        self.upload_button['state'] = tk.DISABLED
        self.save_button['state'] = tk.DISABLED
        self.upload_in_progress = 1
        # TODO: upload timesheet
        print("Uploading file...")
        print(self.file)
        self.saved_time_label.config(text="uploading...")
        self.upload_button.after(4000, self.handler_upload_complete)

    def handler_upload_complete(self):
        self.upload_button['state'] = tk.NORMAL
        self.save_button['state'] = tk.NORMAL
        self.saved_time_label.config(text="error")
        self.upload_in_progress = 0
        self.upload_button.after(2000, lambda: self.saved_time_label.config(text=""))

    def save_file(self, seconds_to_add):
        if self.upload_in_progress == 1:
            return
        self.file_lines = []
        with open(self.file, "r") as f:
            for line in f:
                self.file_lines.append(line)

        parts = self.file_lines[-1].split(',')
        date_part = parts[0]
        time_part = parts[1].strip()

        file_dt = datetime.datetime.strptime(date_part, "%m/%d/%Y")
        now_dt = datetime.datetime.now()

        if file_dt.date() == now_dt.date():
            entry = []
            entry.append(now_dt.strftime('%m/%d/%Y'))
            time_part_parts = time_part.split(':')
            time_part_in_seconds = datetime.timedelta(hours=int(time_part_parts[0]), minutes=int(time_part_parts[1]), seconds=int(time_part_parts[2]))
            entry.append(time.strftime('%H:%M:%S', time.gmtime(seconds_to_add + time_part_in_seconds.total_seconds())))
            self.file_lines[-1] = entry[0] + ", " + entry[1] + "\n"

            with open(self.file, 'w') as f:     # overwrite file
                for line in self.file_lines:
                    f.write(line)
        else:
            entry = []
            entry.append(now_dt.strftime('%m/%d/%Y'))
            entry.append(time.strftime('%H:%M:%S',time.gmtime(seconds_to_add)))
            self.file_lines.append(entry[0] + ", " + entry[1] + "\n")

            with open(self.file, 'a') as f:     # append file
                f.write(self.file_lines[-1])

        self.saved_time_label.config(text="+" + time.strftime('%H:%M:%S',time.gmtime(seconds_to_add)))
        self.saved_time_label.after(6000, lambda: self.saved_time_label.config(text=""))

    def Start(self):
        self.root.mainloop()

timelog = Timelog()
timelog.Start()