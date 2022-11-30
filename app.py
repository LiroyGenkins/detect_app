from __future__ import print_function
import tkinter as tki
from detect import Detector
from PIL import Image
from PIL import ImageTk
import imutils
import threading
import datetime
from imutils.video import VideoStream
import cv2
import os
import subprocess
import time

class App(tki.Tk):
    def __init__(self, outputPath):
        super().__init__()
        self.Run_server()
        self.vs = VideoStream(r"rtmp://127.0.0.1:1935/live/1").start()
        time.sleep(2)
        self.outputPath = outputPath
        self.frame = None
        self.detection = False
        self.thread = None
        self.stopEvent = None
        self.vid = None
        self.title('Распознаватель техники')
        self.geometry('1200x500')
        self.config(bg='#AAAAAA')

        self.vid_frame = tki.Label().grid(column=0, row=0, rowspan=2, columnspan=4, sticky="nswe")

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.btn = tki.Button(self, text='Распознать с дрона', background='gray', font='Arial 12')
        self.snap = tki.Button(self, text="Сделать снимок", background='gray', font='Arial 12')
        self.btn.bind("<Button-1>", self.start_detection)
        self.snap.bind("<Button-1>", self.takeSnapshot)
        self.btn.grid(column=6, row=0, sticky="nswe")
        self.snap.grid(column=7, row=0, sticky="nswe")
        self.textbox = tki.Text(self, font='Arial 10', wrap='word')
        self.textbox.grid(column=6, row=1, columnspan=2, rowspan=3, sticky="nswe")

        self.wm_protocol("WM_DELETE_WINDOW", self.onClose)


    def Run_server(self):
        self.server = subprocess.Popen('MonaServer.exe')
        print("Something wrong" if self.server.poll() else "Server warmup")
        time.sleep(2)

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=640)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.vid_frame is None:
                    self.vid_frame = tki.Label(image=image)
                    self.vid_frame.image = image
                    self.vid_frame.grid(column=0, row=0, rowspan=2, columnspan=2, sticky="nswe")
                else:
                    self.vid_frame.configure(image=image)
                    self.vid_frame.image = image
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self, event):
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))

        cv2.imwrite(p, self.vid_frame.res_im.copy()) if self.detection else cv2.imwrite(p, self.frame.copy())
        text = open(f'./Results/{filename}.txt', 'w')
        text.write(self.textbox.get('1.0', 'end'))
        text.close()
        print("[INFO] saved {}".format(filename))

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.server.terminate()
        self.quit()

    def start_detection(self, event):
        self.stopEvent.set()
        self.vs.stop()
        self.nametowidget('!label').destroy()

        self.detection = True
        self.vid_frame = Detector(self)
        self.vid_frame.grid(column=0, row=0, rowspan=2, columnspan=4, sticky="nswe")
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.vid_frame.run, args=())
        # self.run(weights="ext_ver.pt", source=r"rtmp://127.0.0.1:1935/live/1", nosave=True)
        self.thread.start()

if __name__ == '__main__':
    app = App('./Results')
    app.mainloop()