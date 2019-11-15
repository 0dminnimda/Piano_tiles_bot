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
cv.createTrackbar("from hight", "Tracking", 43, 800, nothing)
cv.createTrackbar("to hight", "Tracking", 724, 1440, nothing)
cv.createTrackbar("from width", "Tracking", 420, 900, nothing)
cv.createTrackbar("to width", "Tracking", 800, 2560, nothing)

top = cv.getTrackbarPos("from hight", "Tracking")
left = cv.getTrackbarPos("from width", "Tracking")
width = cv.getTrackbarPos("to width", "Tracking")-left
height = cv.getTrackbarPos("to hight", "Tracking")-top
cv.destroyAllWindows()

mou = 0
add_v = 0
st = time.time()

while 1:
    add_v = 0
    mou += 1
    mou %= 2
    press = None
    press2 = None
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    if press == '3':
        print("finishing", time.time()-st)
        break
    elif press == '9':
        print("new game", time.time()-st)
        for i in range(4):
            if bool(mou) is True:
                mouse.position = (485+100*i, 500)
                mouse.click(Button.left, 1)

        while 1:
            listener = keyboard.Listener(
                on_press = on_press2, 
                on_release = on_release)
            listener.start()
            if press2 == '6':
                print("stop game", time.time()-st)
                cv.destroyAllWindows()
                keyboard.Listener.stop(listener)
                break

            if (time.time() - st)%2 <= 0.06 and press2 == "д":
                press2 = None
                add_v += 1
                print("added", time.time()-st)

            if bool(mou) is True:
                img1 = np.array(sct.grab({'top': top, 'left': left, 'width': width, 'height': height}))
            else:
                img1 = cv.imread("img.jpg")

            img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

            _, tra = cv.threshold(img, 20, 255, 1)

            contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            #cv.drawContours(img1, contour, -1, (0,0,255))
            for cnt in contour:
                area = cv.contourArea(cnt)
                if area > 1000:
                    x, y, w, h = cv.boundingRect(cnt)
                    x1 = x+0.5*w
                    y1 = y+0.97*h + add_v*10#h*cv.getTrackbarPos("val", "Tracking")
                    #cv.circle(img1,(int(x1),int(y1)),15,(0,255,255), 2)
                    #cv.rectangle (img1, (x, y), (x + w, y + h), (0,255,0), 2)
                    if bool(mou) is True:
                        mouse.position = (x1+left, y1+top)
                        mouse.click(Button.left, 1)

            #cv.imshow("img", img1)
            #cv.imshow("img2", tra)
            if cv.waitKey(1) & 0xFF == ord('2'):
                cv.destroyAllWindows()
                break
            pass
            