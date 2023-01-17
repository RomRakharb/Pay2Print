import keyboard
import win32print
import serial
import tkinter as tk
from tkinter import ttk
import threading
import time

min_v = 1000
printer_status = 1
total_bath = 0


def printer_control():
    global printer_status
    total_pages = 0
    for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
        flags, desc, name, comment = p
        phandle = win32print.OpenPrinter(name)
        print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
        for job in print_jobs:
            total_pages += job['TotalPages']
            # pause job 1
            # print 2
            # cancel 3
            win32print.SetJob(phandle, job['JobId'], 0, None, printer_status)
    return total_pages


def read_serial():
    while True:
        global min_v, total_bath
        with serial.Serial('COM3', 9600) as ser:
            x = ser.readline()
        count = str(x).replace("b'", '').replace(' ', '').replace("\\r\\n'", '')
        try:
            if int(count) < 100:
                total_bath += 1
        except ValueError:
            pass


class PayWindow:
    def __init__(self, page):
        self.page = page

    def disable_closing(self):
        keyboard.add_hotkey("alt + f4", lambda: None, suppress=True)
        # keyboard.add_hotkey("alt + tab", lambda: None, suppress=True)
        # keyboard.add_hotkey("ctrl + shift + esc", lambda: None, suppress=True)
        # keyboard.add_hotkey("windows + tab", lambda: None, suppress=True)

        # keyboard.remove_hotkey("alt + tab")

    def on_cancel(self, win):
        win.destroy
        return 3


    def window(self):
        win = tk.Tk()
        global total_bath
        win.attributes('-fullscreen', True)
        win.title('Pay2Print')
        self.disable_closing()

        button_style = ttk.Style()
        button_style.configure('my.TButton', font=("TH Sarabun New", 50))

        label_style = ttk.Style()
        label_style.configure('my.TLabel', font=("TH Sarabun New", 50))

        page_left = ttk.Label(win, text=f"คงเหลือ {self.page - total_bath} บาท", style='my.TLabel')

        cancel_button = ttk.Button(win, text='ยกเลิก', style='my.TButton', command=self.on_cancel(win))

        page_left.pack(expand=True)
        cancel_button.pack(expand=True)

        if self.page - total_bath <= 0:
            win.destroy
            return 2

        win.mainloop()


if __name__ == "__main__":
    x = threading.Thread(target=read_serial)
    x.start()
    while True:
        if printer_control():
            time.sleep(1)
            start = PayWindow(printer_control())
            if start.window():
                pass

    # while True:
    #     read_serial()
    # pass
