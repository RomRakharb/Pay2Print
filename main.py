import keyboard
import win32print
import serial
import threading
import time
import PySimpleGUI as sg


class Printer:
    @staticmethod
    def init():
        print('enter init')
        while True:
            for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
                flags, desc, name, comment = p
                phandle = win32print.OpenPrinter(name)
                print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
                for job in print_jobs:
                    win32print.SetJob(phandle, job['JobId'], 0, None, 1)
                    if job['Status'] != 1:
                        print(job['TotalPages'])
                        time.sleep(1)
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
        i = 0
        font = ("Arial", 50)
        layout = [
            [sg.Text('จำนวนหน้า', font=font)],
            [sg.Text(i, font=font, key='i')],
            [sg.Button('ยกเลิก', font=font)]
        ]
        window = sg.Window('Title', layout, no_titlebar=True, element_justification='center',
                           finalize=True)
        window.Maximize()
        while True:
            event, values = window.read(timeout=10)
            if event == sg.WIN_CLOSED or event == 'ยกเลิก':
                print('break')
                break
            i += 1
            window['i'].update(i)
            time.sleep(1)
        window.close()


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


if __name__ == "__main__":
    Window.pay()
    pass
    # phandle, job = Printer.init()
    # print(job)
