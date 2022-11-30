from __future__ import print_function
import tkinter as tki
from detect import Detector
from PIL import Image
from PIL import ImageTk
import threading
import datetime
from imutils.video import VideoStream
import imutils
import cv2
import os
import subprocess
import time

class App(tki.Tk):
    def __init__(self, outputPath):
        super().__init__()
        self.Run_server()
        self.vs = VideoStream(r"rtmp://127.0.0.1:1935/live/1").start()
        time.sleep(2.0)
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        # initialize the root window and image panel
        self.panel = None
        self.title('Распознаватель техники')
        self.geometry('1250x650')
        self.config(bg='#AAAAAA')
        self.add_frames()

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        # set a callback to handle when the window is closed
        self.wm_protocol("WM_DELETE_WINDOW", self.onClose)


    def Run_server(self):
        self.server = subprocess.Popen('MonaServer.exe')
        print("Что-то не так" if self.server.poll() else "Сервер поднялся")
        time.sleep(5)

    def update(self):
        self.after(10, self.update)

    def refresh(self):
        name = self.children[[f for f in self.children if f.find('!textframe') != -1][0]]
        print(name)
        self.nametowidget(name).destroy()
        self.text_frame = TextFrame(self)
        self.text_frame.grid(column=0, row=1, sticky="nswe")

    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=640)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.vid_frame is None:
                    self.vid_frame = tki.Label(image=image)
                    self.vid_frame.image = image
                    self.vid_frame.grid(column=1, row=0, rowspan=2, sticky="nswe")

                # otherwise, simply update the panel
                else:
                    self.vid_frame.configure(image=image)
                    self.vid_frame.image = image
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self, event):
        # grab the current timestamp and use it to construct the
        # output path
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))
        # save the file
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.server.terminate()
        self.quit()

    def add_frames(self):
        self.text_frame = TextFrame(self)
        self.text_frame.grid(column=0, row=1, sticky="nswe")
        # self.vid_frame = Detector(self)
        self.vid_frame = tki.Label()
        self.vid_frame.grid(column=1, row=0, rowspan=2, sticky="nswe")
        self.panel_frame = PanelFrame(self).grid(column=0, row=0, sticky="nswe")

    def start_detection(self, event):
        self.text_frame.textbox.insert('end', "Кнопка")
        #self.refresh()


class PanelFrame(tki.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.high = 50
        self.width = 400
        self.btn = tki.Button(self, text='Распознать с дрона', height=3, background='gray', font='Arial 14')
        self.snap = tki.Button(self, text="Сделать снимок", height=2, background='gray', font='Arial 14')
        self.off = tki.Button(self, text='Закончить распознавание', height=2, background='gray', font='Arial 14')
        self.btn.bind("<Button-1>", self.master.start_detection)
        self.snap.bind("<Button-1>", self.master.takeSnapshot)
        self.off.bind("<Button-1>", self.End_detect)
        self.btn.pack(side='top', fill='both')
        self.snap.pack(side='top', fill='both')
        self.off.pack(side='top', fill='both')

    def End_detect(self, event):
        print('хер')
        self.master.server.terminate()

class TextFrame(tki.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.high = 100
        self.width = 400
        self.textbox = tki.Text(self, font='Arial 10', wrap='word')
        self.textbox.pack()


if __name__ == '__main__':
    app = App('./Results')
    app.mainloop()