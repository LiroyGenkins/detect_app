#from detect import *
import torch 
import os
import cv2
from detect import run


path_video = r"rtmp://127.0.0.1:1935/live/1"
#path_video = r"https://www.youtube.com/watch?v=tGvS0XOlhfQ"

model_name = r"ext_ver.pt"



def detect():
    run(weights=model_name, source= path_video, nosave=True)

    #model = torch.hub.load(os.getcwd(), 'custom', source='local', path = model_name, force_reload = True)
         
    #vid_capture = cv2.VideoCapture(path_video)

    # if (not vid_capture.isOpened()):
    #     print("Error\n")
    #     return
    # stack = 0
    # while(vid_capture.isOpened()):
    #     print(stack)
    #     if stack > 5:
    #         stack = 0
    #         ret, frame = vid_capture.read()
    #         results = model(frame)
    #
    #         cv2.imshow('Test', results.render()[0])
    #         # if ret:
    #         #
    #         #     # if cv2.waitKey(22) & 0xFF == ord('q'):
    #         #     #     break
    #         # else:
    #         #     break
    #     else:
    #         stack += 1
    #
    #
    # vid_capture.release()
    # cv2.destroyAllWindows()
        


def main():
    detect()

if __name__ == "__main__":
    main()
    
    
    
    