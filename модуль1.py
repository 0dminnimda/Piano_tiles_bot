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

def test1(nn):
    init_tr()
    num_y = cv.getTrackbarPos("num_y", "Tracking1")
    num_x = cv.getTrackbarPos("num_x", "Tracking1")
    top, height, left, width, shift_y, shift_x = get_tr(num_y, num_x)
    cv.destroyAllWindows()

    arr = []
    for _ in range(nn):
        st = time.time()

        for i in range(num_y):
            for j in range(num_x):
                img1 = np.array(sct.grab({'top': top[i], 'left': left[j], 'width': width[j]-left[j], 'height': height[i]-top[i]}))

                img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                _, tra = cv.threshold(img, 20, 255, 1)
                contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

                #cv.imshow(f"{(i+1)+(j+1)*10}", img)
                #if cv.waitKey(1) & 0xFF == ord('2'):
                #    cv.destroyAllWindows()
                #    break

        end = time.time()-st
        arr.append(end)
    print(np.array(arr).mean())

def test2(nn):
    init_tr()
    num_y = cv.getTrackbarPos("num_y", "Tracking1")
    num_x = cv.getTrackbarPos("num_x", "Tracking1")
    top, height, left, width, shift_y, shift_x = get_tr(num_y, num_x)
    cv.destroyAllWindows()

    arr = []
    for _ in range(nn):
        st = time.time()

        img1 = np.array(sct.grab({'top': shift_y, 'left': shift_x, 'width': width[-1], 'height': height[-1]}))
        for i in range(num_y):
            for j in range(num_x):
                img = img1[top[i]:height[i], left[j]:width[j]]

                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                _, tra = cv.threshold(img, 20, 255, 1)
                contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        end = time.time()-st
        arr.append(end)
    print(np.array(arr).mean())


def init_tr():
    cv.namedWindow("Tracking1", cv.WINDOW_NORMAL)
    cv.createTrackbar("pos_y", "Tracking1", 53, 500, nothing)
    cv.createTrackbar("pos_x", "Tracking1", 303, 500, nothing)

    cv.createTrackbar("num_y", "Tracking1", 1, 10, nothing)
    cv.createTrackbar("num_x", "Tracking1", 4, 10, nothing)

    cv.createTrackbar("val_y", "Tracking1", 40, 500, nothing)
    cv.createTrackbar("val_x", "Tracking1", 40, 500, nothing)

    cv.createTrackbar("dist_y", "Tracking1", 123, 200, nothing)
    cv.createTrackbar("dist_x", "Tracking1", 75, 200, nothing)

    cv.createTrackbar("shift_y", "Tracking1", 20, 500, nothing)
    cv.createTrackbar("shift_x", "Tracking1", 0, 500, nothing)
    pass

def get_tr(num_y, num_x):
    pos_y = cv.getTrackbarPos("pos_y", "Tracking1")
    val_y = cv.getTrackbarPos("val_y", "Tracking1")
    shift_y = cv.getTrackbarPos("shift_y", "Tracking1")
    dist_y = cv.getTrackbarPos("dist_y", "Tracking1")

    pos_x = cv.getTrackbarPos("pos_x", "Tracking1")
    val_x = cv.getTrackbarPos("val_x", "Tracking1")
    shift_x = cv.getTrackbarPos("shift_x", "Tracking1")
    dist_x = cv.getTrackbarPos("dist_x", "Tracking1")

    top = [pos_y for i in range(num_y)]
    for i in range(len(top)):
        if i != 0:
            top[i] += dist_y*i
    height = [top[i]+val_y for i in range(num_y)]

    left = [pos_x for i in range(num_x)]
    for i in range(len(left)):
        if i != 0:
            left[i] += dist_x*i
    width = [left[i]+val_x for i in range(num_x)]

    return  top, height, left, width, shift_y, shift_x

init_tr()
num_y = cv.getTrackbarPos("num_y", "Tracking1")
num_x = cv.getTrackbarPos("num_x", "Tracking1")
top, height, left, width, shift_y, shift_x = get_tr(num_y, num_x)

while 0:
    num_y = cv.getTrackbarPos("num_y", "Tracking1")
    num_x = cv.getTrackbarPos("num_x", "Tracking1")
    top, height, left, width, shift_y, shift_x = get_tr(num_y, num_x)

    img1 = np.array(sct.grab({'top': shift_y, 'left': shift_x, 'width': width[-1], 'height': height[-1]}))
    #print(img1.shape)
    for i in range(num_y):
        for j in range(num_x):
            img = img1[top[i]:height[i], left[j]:width[j]]
            #print(img.shape)

            cv.imshow(f"{(i+1)+(j+1)*10}", img)

    if cv.waitKey(1) & 0xFF == ord('2'):
        cv.destroyAllWindows()
        break

test1(50)
test2(50)