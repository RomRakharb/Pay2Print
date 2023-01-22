import keyboard
import win32print
import serial
import threading
import time
import PySimpleGUI as sg

total_pages = 0
total_bath = 0
class Printer:
    @staticmethod
    def init():
        global total_pages
        print('enter init')
        while True:
            for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
                flags, desc, name, comment = p
                phandle = win32print.OpenPrinter(name)
                print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
                for job in print_jobs:
                    win32print.SetJob(phandle, job['JobId'], 0, None, 1)
                    if job['Status'] != 1:
                        total_pages = job['TotalPages']
                        continue
                    return phandle, job

    @staticmethod
    def printing(phandle, job_id):
        win32print.SetJob(phandle, job_id, 0, None, 2)

    @staticmethod
    def cancel(phandle, job_id):
        win32print.SetJob(phandle, job_id, 0, None, 3)


class Window:
    @staticmethod
    def init():
        layout = [
            [sg.Text('Choose port')]
        ]
        window = sg.Window('Title', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
        window.close()

    @staticmethod
    def pay():
        global total_pages
        font = ("Arial", 50)

        elements = [
            [sg.Text('จำนวนหน้า', font=font)],
            [sg.Text(total_pages, font=font, key='TotalPages', border_width=100)],
            [sg.Button('ยกเลิก', font=font)]
        ]

        layout = [[sg.VPush()],
                  [sg.Push(), sg.Column(elements, element_justification='c'), sg.Push()],
                  [sg.VPush()]]
        window = sg.Window('Title', layout, no_titlebar=True, finalize=True)
        window.Maximize()
        while True:
            event, values = window.read(timeout=10)
            if event == sg.WIN_CLOSED or event == 'ยกเลิก':
                print('close')
                break
            window['TotalPages'].update(total_pages)
            time.sleep(1)
        window.close()


def read_serial():
    global total_bath
    with serial.Serial('COM3', 9600) as ser:
        x = ser.readline()
    count = str(x).replace("b'", '').replace(' ', '').replace("\\r\\n'", '')
    try:
        if int(count) < 100:
            total_bath += 1
    except ValueError:
        pass


if __name__ == "__main__":
    threading.Thread(target=Printer.init).start()
    while True:
        if total_pages > 0:
            Window.pay()
            break
            # print(f"The total pages is {total_pages}")
            # time.sleep(1)
    # phandle, job = Printer.init()
    # print(job)
