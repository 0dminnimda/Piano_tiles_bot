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

def init_tr():
    cv.namedWindow("Tracking1", cv.WINDOW_NORMAL)
    cv.createTrackbar("num", "Tracking1", 4, 10, nothing)
    cv.createTrackbar("val", "Tracking1", 40, 200, nothing)
    cv.createTrackbar("dist", "Tracking1", 123, 200, nothing)
    cv.createTrackbar("shift", "Tracking1", 0, 500, nothing)

    cv.createTrackbar("from_width", "Tracking1", 303, 900, nothing)
    cv.createTrackbar("to_width", "Tracking1", 580, 2560, nothing)
    pass

def get_tr(num):
    top = [53 for i in range(num)]
    height = [53-top[i]+cv.getTrackbarPos("val", "Tracking1") for i in range(num)]
    left = cv.getTrackbarPos("from_width", "Tracking1")
    width = cv.getTrackbarPos("to_width", "Tracking1")-left

    shift = cv.getTrackbarPos("shift", "Tracking1")
    dist = cv.getTrackbarPos("dist", "Tracking1")
    for i in range(len(top)):
        top[i] += shift
        if i != 0:
            top[i] += dist*i

    return  top, height, left, width

mou = 1
init_tr()
num = cv.getTrackbarPos("num", "Tracking1")
top, height, left, width = get_tr(num)
#cv.destroyAllWindows()

while 1:
    add_v = 0
    press = None
    press2 = None
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    st = time.time()
    if (press == 'й' or press == 'q'):
        st = time.time()
        print("new game", time.time()-st)
        for i in range(4):
            if mou == 0:
                mouse.position = (485+100*i, 500)
                mouse.click(Button.left, 1)
        time.sleep(0.1)

        while 1:
            num = cv.getTrackbarPos("num", "Tracking1")
            top, height, left, width = get_tr(num)
            listener = keyboard.Listener(
                on_press = on_press2, 
                on_release = on_release)
            listener.start()
            if (press2 == 'ц' or press2 == 'w'):
                print("stop game", time.time()-st)
                cv.destroyAllWindows()
                keyboard.Listener.stop(listener)
                init_tr()
                break

            if (time.time() - st)%2 <= 0.06 and (press2 == "ы" or press2 == "s"):
                press2 = None
                add_v += 1
                print("added", time.time()-st)
                #1-375; 2-3

            for i in range(num):
                img1 = np.array(sct.grab({'top': top[i], 'left': left, 'width': width, 'height': height[i]}))

                img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

                _, tra = cv.threshold(img, 20, 255, 1)

                contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                #cv.drawContours(img1, contour, -1, (0,0,255))
                for cnt in contour:
                    area = cv.contourArea(cnt)
                    if area > 250:
                        x, y, w, h = cv.boundingRect(cnt)
                        x1 = x+0.5*w
                        y2 = y+0.5*h
                        y1 = y+0.95*h + add_v*5
                        cv.circle(img1,(int(x1),int(y1)),15,(0,255,255), 2)
                        #cv.rectangle(img1, (x, y), (x + w, y + h), (0,255,0), 2)
                        cv.putText(img1, "%d" % h, (int(x1)-30, int(y2)), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if mou == 0:
                            mouse.position = (x1+left[i], y1+top[i]) # x1+left, y1+top
                            mouse.click(Button.left, 1)

                cv.imshow(f"img{i}", img1)
                #cv.imshow("img2", tra)
                if cv.waitKey(1) & 0xFF == ord('2'):
                    cv.destroyAllWindows()
                    break

    elif (press == 'у' or press == 'e'):
        print("finishing", time.time()-st)
        break