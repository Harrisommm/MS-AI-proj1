from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from ultralytics import YOLO
import cv2
import threading
import time


end_frame_file = './temp/end_frame.txt'
video_path_file = './temp/video_path.txt'

# Create your views here.
def home_main(request):
    return render(request, 'home_main.html')

def move_page1(request):
    video_name = "./static/test_video/test1.mp4"
    try:
        with open(video_path_file, 'w') as file:
            file.write(str(video_name))
    except FileNotFoundError:
        print('읽어오기 실패')
        pass
    return render(request, 'video_test.html')

def move_page2(request):
    video_name = "./static/test_video/test2.mp4"
    try:
        with open(video_path_file, 'w') as file:
            file.write(str(video_name))
    except FileNotFoundError:
        print('읽어오기 실패')
        pass
    return render(request, 'video_test.html')

def move_page3(request):
    video_name = "./static/test_video/test3.mp4"
    try:
        with open(video_path_file, 'w') as file:
            file.write(str(video_name))
    except FileNotFoundError:
        print('읽어오기 실패')
        pass
    return render(request, 'video_test.html')

def move_page4(request):
    video_name = "./static/test_video/test4.mp4"
    try:
        with open(video_path_file, 'w') as file:
            file.write(str(video_name))
    except FileNotFoundError:
        print('읽어오기 실패')
        pass
    return render(request, 'video_test.html')

def stream(frame_num, cap):
    while cap.isOpened():
        #첫 프레임 위치를 가져옴
        frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) + 1
        ret, frame = cap.read()

        if not ret:
            # ret이 false(마지막 프레임 재생 후 frame_num 0으로 초기화)
            frame_num=0
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num) +1
            ret, frame = cap.read()

        cv2.imwrite('./temp/video1.jpg', frame)
        if cv2.waitKey(20)==27:
            break
        frame_count = frame_count + 1
        with open(end_frame_file, 'w') as file:
            file.write(str(frame_count))

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + open('./temp/video1.jpg', 'rb').read() + b'\r\n')
            


        
@gzip.gzip_page
def video(request):
    try:
        with open(end_frame_file, 'r') as file:
            frame_num = int(file.read())
    except FileNotFoundError:
        print('읽어오기 실패')
        pass
    
    # 비디오 불러오기
    cap=cv2.VideoCapture(video_path)
    # frame_num부터 재생 시작
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    try:
        # stream 함수에 frame_num, cap 전달
        output = stream(frame_num, cap)
        return StreamingHttpResponse(output, content_type="multipart/x-mixed-replace;boundary=frame")
    except: # This is bad! replace it with proper handling
        print("error..")
        pass


