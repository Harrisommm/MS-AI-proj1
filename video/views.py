from django.shortcuts import render

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from ultralytics import YOLO
import cv2
import threading
import time

model = YOLO("./model/best.pt")
video_path_file = "./temp/video_path.txt"
end_frame_file = './temp/end_frame.txt'

# ------------------------------------------------

# def detect(ret, frame):
#     if (ret is True) :
#         results = model.track(frame, persist=True)

#         detect_frame = results[0].plot()
#         detect_frame = cv2.resize(detect_frame, (640, 480))
#         return detect_frame

def stream(cap):
    model = YOLO("./model/best.pt")
    while cap.isOpened():
        #첫 프레임 위치를 가져옴
        # frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) + 1
        ret, frame = cap.read()
        # frame_ = detect(ret, frame)
        results = model.track(frame, persist=True)

        frame_ = results[0].plot()
        
        
        if not ret:
            # ret이 false(마지막 프레임 재생 후 frame_num 0으로 초기화)
            # frame_num=0
            # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num) +1
            ret, frame = cap.read()

        cv2.imwrite('./temp/detect_image.jpg', frame_)
        if cv2.waitKey(1)==27:
            break
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + open('./temp/detect_image.jpg', 'rb').read() + b'\r\n')
        
@gzip.gzip_page
def video(request):

    # try:
    #     with open(end_frame_file, 'r') as file:
    #         frame_num = int(file.read())
    # except FileNotFoundError:
    #     print('읽어오기 실패')
    #     pass
    try:
        with open(video_path_file, 'r') as file:
            path = str(file.read())
    except FileNotFoundError:
        print('읽어오기 실패')
        pass

    # 비디오 불러오기
    cap=cv2.VideoCapture(path)
    # frame_num부터 재생 시작
    # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    try:
        # stream 함수에 frame_num, cap 전달
        output = stream(cap)
        return StreamingHttpResponse(output, content_type="multipart/x-mixed-replace;boundary=frame")
    except: # This is bad! replace it with proper handling
        print("error..")
        pass


