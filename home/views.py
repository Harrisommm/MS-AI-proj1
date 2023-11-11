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