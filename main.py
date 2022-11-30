# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from kivy.app import App
import multiprocessing
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import subprocess
import time
import cv2
import recogn



class MainApp(App):
    def close_application(self):
        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()

    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        button = Button(text='Распознать', size_hint=(.8, .2), pos_hint={'center_x': .5, 'center_y': .5})
        button.bind(on_press=self.on_press_button)
        main_layout.add_widget(button)
        self.res = TextInput(multiline=True, readonly=True, font_size=14, size_hint=(1, .2))
        #self.img = Image(source='prev.jpg')
        main_layout.add_widget(self.res)
        #main_layout.add_widget(self.img)
        return main_layout

    def on_press_button(self, instace):
        pass
        # vid_capture = cv2.VideoCapture(r"rtmp://127.0.0.1:1935/live/1")
        # if (vid_capture.isOpened() == False):
        #     print("Ошибка открытия видеофайла")
        # while (vid_capture.isOpened()):
        #     ret, frame = vid_capture.read()
        #     if ret == True:
        #         cv2.imshow('Look', frame)
        #         key = cv2.waitKey(20)
        #         if (key == ord('q')) or key == 27:
        #             break
        #     else:
        #         break
        # vid_capture.release()
        # cv2.destroyAllWindows()


        #p = multiprocessing.Process(target=recogn.detect())
        #p.start()
        #self.res.text = desc.description['т72б'] if proc.res[0] else desc.description['other']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = MainApp()
    server = subprocess.Popen('MonaServer.exe')
    print(server.poll())
    time.sleep(5)
    app.run()
    server.terminate()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
