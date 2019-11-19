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
    shift = cv.getTrackbarPos("shift", "Tracking1")
    dist = cv.getTrackbarPos("dist", "Tracking1")

    top = [53 for i in range(num)]
    for i in range(len(top)):
        if i != 0:
            top[i] += dist*i

    height = [top[i]+val for i in range(num)]
    left = cv.getTrackbarPos("from_width", "Tracking1")
    width = cv.getTrackbarPos("to_width", "Tracking1")-left

    return  top, height, left, width, shift


def test1(nn):
    init_tr()
    num = cv.getTrackbarPos("num", "Tracking1")
    top, height, left, width, shift = get_tr(num)
    cv.destroyAllWindows()

    arr = []
    for _ in range(nn):
        st = time.time()

        for i in range(num):
            img1 = np.array(sct.grab({'top': top[i], 'left': left, 'width': width, 'height': height[i]}))
            #cv.imshow(f"i{i}", img1)
            #if cv.waitKey(1) & 0xFF == ord('2'):
            #    cv.destroyAllWindows()
            #    break

            img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            _, tra = cv.threshold(img, 20, 255, 1)
            contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        end = time.time()-st
        arr.append(end)
    print(np.array(arr).mean())

def test2(nn):
    init_tr()
    num = cv.getTrackbarPos("num", "Tracking1")
    top, height, left, width, shift = get_tr(num)
    cv.destroyAllWindows()

    arr = []
    for _ in range(nn):
        st = time.time()

        img1 = np.array(sct.grab({'top': shift, 'left': left, 'width': width, 'height': height[-1]}))
        for i in range(num):
            img = img1[top[i]:height[i]]

            #cv.imshow(f"i2{i}", img)
            #if cv.waitKey(1) & 0xFF == ord('2'):
            #    cv.destroyAllWindows()
            #    break

            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            _, tra = cv.threshold(img, 20, 255, 1)
            contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        end = time.time()-st
        arr.append(end)
    print(np.array(arr).mean())

init_tr()
num = cv.getTrackbarPos("num", "Tracking1")
top, height, left, width, shift = get_tr(num)

while 0:
    num = cv.getTrackbarPos("num", "Tracking1")
    top, height, left, width, shift = get_tr(num)

    img1 = np.array(sct.grab({'top': shift, 'left': left, 'width': width, 'height': height[-1]}))
    #print(img1.shape)
    for i in range(num):
        img = img1[top[i]:height[i]]
        #print(img.shape)

        cv.imshow(f"img{i}", img)
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break

test1(50)
test2(50)