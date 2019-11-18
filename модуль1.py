import numpy as np
import cv2 as cv
from mss import mss
from pynput import keyboard
from pynput.mouse import Button, Controller
import time

def nothing(x):
    pass

mouse = Controller()
sct = mss()

def init_tr():
    cv.namedWindow("Tracking1", cv.WINDOW_NORMAL)
    cv.createTrackbar("num", "Tracking1", 4, 10, nothing)
    cv.createTrackbar("val", "Tracking1", 20, 200, nothing)
    cv.createTrackbar("dist", "Tracking1", 123, 200, nothing)
    cv.createTrackbar("shift", "Tracking1", 0, 500, nothing)

    cv.createTrackbar("from_width", "Tracking1", 303, 900, nothing)
    cv.createTrackbar("to_width", "Tracking1", 580, 2560, nothing)
    pass

def get_tr(num):
    val = cv.getTrackbarPos("val", "Tracking1")
    top = [53 for i in range(num)]
    height = [53-top[i]+val for i in range(num)]
    left = cv.getTrackbarPos("from_width", "Tracking1")
    width = cv.getTrackbarPos("to_width", "Tracking1")-left

    shift = cv.getTrackbarPos("shift", "Tracking1")
    dist = cv.getTrackbarPos("dist", "Tracking1")
    for i in range(len(top)):
        top[i] += shift
        if i != 0:
            top[i] += dist*i
                
    return  top, height, left, width, shift, val

init_tr()
num = cv.getTrackbarPos("num", "Tracking1")
top, height, left, width, shift, val = get_tr(num)

for _ in range(1):
    st1 = time.time()
    for i in range(num):
        img1 = np.array(sct.grab({'top': top[i], 'left': left, 'width': width, 'height': height[i]}))
        img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        _, tra = cv.threshold(img, 20, 255, 1)
        contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    end1 = time.time()-st1
    print(end1)

    st11 = time.time()
    for i in range(num):
        img1 = np.array(sct.grab({'top': top[i], 'left': left, 'width': width, 'height': height[i]}))
        img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        _, tra = cv.threshold(img, 20, 255, 1)
        contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    end11 = time.time()-st1
    print(end11)
    print((end11+end1)/2)

    st2 = time.time()

while 1:
    num = cv.getTrackbarPos("num", "Tracking1")
    top, height, left, width, shift, val = get_tr(num)
    img1 = np.array(sct.grab({'top': shift, 'left': left, 'width': width, 'height': top[-1]+shift+val}))
    cv.imshow("img", img1)
    print(img1.shape[1], width, left)
    for i in range(num):
        t = top[i]
        img = img1[t:t+val, 0:width]
        if img.shape[0] > 0 and img.shape[1] > 0:
            cv.imshow(f"img{i}", img)
        else:
            print(f"wr sizes{i}",top[i],top[i]+height[i])
            pass
        
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break