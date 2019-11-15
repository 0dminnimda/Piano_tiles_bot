import numpy as np
import cv2 as cv
from mss import mss
from pynput import keyboard
from pynput.mouse import Button, Controller
import time

def on_press(key):
    global press
    try:
        press = key.char
    except AttributeError:pass

def on_press2(key):
    global press2
    try:
        press2 = key.char
    except AttributeError:pass

def on_release(key):
    if key:
        return False

def nothing(x):
    pass

mouse = Controller()
sct = mss()

cv.namedWindow("Tracking", cv.WINDOW_NORMAL)
cv.createTrackbar("from hight", "Tracking", 45, 800, nothing)
cv.createTrackbar("to hight", "Tracking", 755, 1440, nothing)
cv.createTrackbar("from width", "Tracking", 440, 900, nothing)
cv.createTrackbar("to width", "Tracking", 840, 2560, nothing)

top = cv.getTrackbarPos("from hight", "Tracking")
left = cv.getTrackbarPos("from width", "Tracking")
width = cv.getTrackbarPos("to width", "Tracking")-left
height = cv.getTrackbarPos("to hight", "Tracking")-top
cv.destroyAllWindows()

while 1:
    press = None
    press2 = None
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    if press == '3':
        break
    elif press == '9':
        for i in range(4):
            mouse.position = (485+100*i, 500)
            mouse.click(Button.left, 1)

        while 1:
            listener = keyboard.Listener(
                on_press = on_press2, 
                on_release = on_release)
            listener.start()
            if press2 == '6':
                cv.destroyAllWindows()
                keyboard.Listener.stop(listener)
                break

            #img1 = cv.imread("img.jpg")
            img1 = np.array(sct.grab({'top': top, 'left': left, 'width': width, 'height': height}))

            img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

            _, tra = cv.threshold(img, 20, 255, 1)

            contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            #cv.drawContours(img1, contour, -1, (0,0,255))
            for cnt in contour:
                area = cv.contourArea(cnt)
                if area > 1000:
                    M = cv.moments(cnt)
                    x = int(M['m10']/area)
                    y = int(M['m01']/area)
                    cv.circle(img1,(x,y),15,(0,255,255), 2)
                    mouse.position = (x+left, y+top)
                    mouse.click(Button.left, 1)

            cv.imshow("img2", tra)
            cv.imshow("img", img1)
            if cv.waitKey(1) & 0xFF == ord('2'):
                cv.destroyAllWindows()
                break
            