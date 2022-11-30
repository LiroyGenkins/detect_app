from tkinter import *
import subprocess
import os
import time

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Распознаватель техники')
        self.geometry('1250x650')
        self.config(bg='#AAAAAA')

        self.Run_server()
        self.add_frames()

    def Run_server(self):
        self.server = subprocess.Popen('MonaServer.exe')
        print("Что-то не так" if self.server.poll() else "Сервер поднялся")
        time.sleep(15)

    def Quit(self):
        self.destroy()

    def add_frames(self):
        self.text_frame = TextFrame(self)
        self.text_frame.grid(column=0, row=1, sticky="nswe")
        self.panel_frame = PanelFrame(self).grid(column=0, row=0, sticky="nswe")


class PanelFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.high = 50
        self.width = 400
        self.btn = Button(self, text='Распознать с дрона', height=3, background='gray', font='Arial 14')
        self.off = Button(self, text='Закончить распознавание', height=2, background='gray', font='Arial 14')
        self.btn.bind("<Button-1>", self.start_detection)
        self.off.bind("<Button-1>", self.End_detect)
        self.btn.pack(side='top', fill='both')
        self.off.pack(side='top', fill='both')

    def start_detection(self, event):
        subprocess.run(["ls", "-l", r'python ./yolov5-master/detect.py --weights ext_ver.pt --source rtmp://127.0.0.1:1935/live/1 --nosave'])

    def End_detect(self, event):
        print('хер')
        self.master.server.terminate()
        self.master.Quit()

class TextFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.high = 100
        self.width = 400
        self.textbox = Text(self, font='Arial 10', wrap='word')
        self.textbox.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()