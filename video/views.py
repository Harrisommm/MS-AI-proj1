from django.shortcuts import render

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from ultralytics import YOLO
import cv2
import threading
import time

model = YOLO("./model/best.pt")
video_path = "./test1.mp4"

global prev_time
global  frame_rate
prev_time = 0
frame_rate = 10

def home(request):
    return render(request, 'home.html')
# ------------------------------------------------

def detect(ret, frame):
        
        if (ret is True) :
            prev_time = time.time()
            results = model.track(frame, persist=True)

            detect_frame = results[0].plot()
            detect_frame = cv2.resize(detect_frame, (640, 480))
            return detect_frame

def stream(video_path):
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        current_time = time.time() - prev_time
        if (current_time > 1./ frame_rate) :
            frame_ = detect(ret, frame)
            
            if not ret:
                cap=cv2.VideoCapture(video_path)
                ret, frame = cap.read()
                # frame_ = detect(frame)

            cv2.imwrite('currentframe.jpg', frame_)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('currentframe.jpg', 'rb').read() + b'\r\n')

        
@gzip.gzip_page
def video(request):
    try:
        output = stream()
        return StreamingHttpResponse(output, content_type="multipart/x-mixed-replace;boundary=frame")
    except: # This is bad! replace it with proper handling
        print("error..")
        pass

