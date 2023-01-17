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
total_pages = 0




def printer_control():
    pay = threading.Thread(target=window, daemon=True)
    while True:
        global printer_status, total_pages
        for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
            flags, desc, name, comment = p
            phandle = win32print.OpenPrinter(name)
            print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
            for job in print_jobs:
                win32print.SetJob(phandle, job['JobId'], 0, None, printer_status)
                if not pay.is_alive():
                    print(pay.is_alive())
                    pay.start()
                if job['Status'] != 1:
                    total_pages = job['TotalPages']
                    print(job['TotalPages'])
                    time.sleep(1)
                    continue
                print(job)
                # pause job 1
                # print 2
                # cancel 3


def read_serial():
    global min_v, total_bath
    with serial.Serial('COM3', 9600) as ser:
        x = ser.readline()
    count = str(x).replace("b'", '').replace(' ', '').replace("\\r\\n'", '')
    try:
        if int(count) < 100:
            total_bath += 1
    except ValueError:
        pass


def disable_closing():
    pass
    # keyboard.add_hotkey("alt + f4", lambda: None, suppress=True)
    # keyboard.add_hotkey("alt + tab", lambda: None, suppress=True)
    # keyboard.add_hotkey("ctrl + shift + esc", lambda: None, suppress=True)
    # keyboard.add_hotkey("windows + tab", lambda: None, suppress=True)

    # keyboard.remove_hotkey("alt + tab")


def on_cancel(win):
    win.destroy


def window():
    win = tk.Tk()
    global total_bath, total_pages
    win.attributes('-fullscreen', True)
    win.title('Pay2Print')
    disable_closing()

    button_style = ttk.Style()
    button_style.configure('my.TButton', font=("TH Sarabun New", 50))

    label_style = ttk.Style()
    label_style.configure('my.TLabel', font=("TH Sarabun New", 50))

    page_left = ttk.Label(win, text=f"คงเหลือ {total_pages - total_bath} บาท", style='my.TLabel')
    def on_cancel():
        win.destroy()
        return 3

    cancel_button = ttk.Button(win, text='ยกเลิก', style='my.TButton', command=on_cancel)

    page_left.pack(expand=True)
    cancel_button.pack(expand=True)

    page_left.config(text=f"คงเหลือ {total_pages - total_bath} บาท")
    # if total_pages - total_bath <= 0:
    #     win.destroy
    #     return 2

    win.mainloop()


if __name__ == "__main__":
    # x = threading.Thread(target=read_serial)
    # # x.start()
    printer_control()
    # window()
        # x = printer_control()
        # time.sleep(1)


    # while True:
    #     read_serial()
    # pass
