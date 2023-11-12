from django.shortcuts import render

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from ultralytics import YOLO
import cv2
import threading
import time

model = YOLO("./model/best.pt")
video_path = "./static/test_video/test1.mp4"
detect_status = dict(manhole_closed = None, manhole_hole = None, person= None)
# ------------------------------------------------
@gzip.gzip_page
def video(request):
    try:
        # stream 함수에 frame_num, cap 전달
        output = stream()
        return StreamingHttpResponse(output, content_type="multipart/x-mixed-replace;boundary=frame")
    except: # This is bad! replace it with proper handling
        print("error..")
        pass

def stream():
    cap=cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        # frame_ = detect(ret, frame)
        results = model.track(frame, persist=True)
        if not ret:
            cap=cv2.VideoCapture(video_path)
            # ret이 false(마지막 프레임 재생 후 frame_num 0으로 초기화)
            # frame_num=0
            # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num) +1
            ret, frame = cap.read()
        
        
        frame_ = results[0].plot()
        for r in results :
            boxes = r.boxes.xyxy
            cls = r.boxes.cls
            conf = r.boxes.conf
            cls_dict = r.names
            
            detect_status.update({'manhole_closed':0, 'manhole_hole': 0, 'person': 0})  
            for box, cls_number, conf in zip(boxes, cls, conf) :
                conf_number = float(conf.item())
                cls_number_int = int(cls_number.item())
                cls_name = cls_dict[cls_number_int]
                x1, y1, x2, y2 = box
                
                if cls_number_int == 0:
                    detect_status['manhole_closed'] = 1
                elif cls_number_int == 1:
                    detect_status['manhole_hole'] = 1
                elif cls_number_int == 2:
                    detect_status['person'] = 1
            print(detect_status)
            with open('./temp/detect_status.txt', 'w', encoding='UTF-8') as f:
                for item, status in detect_status.items(): 
                    f.write(f'{item} : {status}\n')
               
            cv2.imwrite('./temp/detect_image.jpg', frame_)
            if cv2.waitKey(1)==27:
                break
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('./temp/detect_image.jpg', 'rb').read() + b'\r\n')  




