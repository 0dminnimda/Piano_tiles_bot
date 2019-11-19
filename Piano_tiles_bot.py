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

    return  top, height, left, width, shift_y, shift_x, dist_x

mou = 0
init_tr()
num_y = cv.getTrackbarPos("num_y", "Tracking1")
num_x = cv.getTrackbarPos("num_x", "Tracking1")
top, height, left, width, shift_y, shift_x, dist_x = get_tr(num_y, num_x)

while 1:
    cv.destroyAllWindows()
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
                mouse.position = (340+70*i, 360)
                mouse.click(Button.left, 1)
        time.sleep(0.1)

        while 1:
            for i in range(num_y-1, -1, -1):
                for j in range(num_x):
                    img1 = np.array(sct.grab({'top': top[i], 'left': left, 'width': width, 'height': height[i]}))

                    img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

                    _, tra = cv.threshold(img, 20, 255, 1)

                    contour, _ = cv.findContours(tra, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                    #cv.drawContours(img1, contour, -1, (0,0,255))
                    for cnt in contour:
                        area = cv.contourArea(cnt)
                        if area > 25:
                            x, y, w, h = cv.boundingRect(cnt)
                            x1 = x+0.5*w
                            y1 = y+0.97*h# + add_v*5
                            #cv.circle(img1,(int(x1),int(y1)),15,(0,255,255), 2)
                            #cv.rectangle(img1, (x, y), (x + w, y + h), (0,255,0), 2)
                            #y2 = y+0.5*h
                            #cv.putText(img1, "%d" % area, (int(x1)-30, int(y2)+7), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                            mouse.position = (x1+left[j], y1+top[i]) # (x1+left, y1+top[i])  x1+left, y1+top
                            mouse.click(Button.left, 1)

                    #cv.imshow(f"img{i}", img1)
                    #cv.imshow("img2", tra)
                    #if cv.waitKey(1) & 0xFF == ord('2'):
                    #    cv.destroyAllWindows()
                    #    break

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

            #if (time.time() - st)%2 <= 0.06 and (press2 == "ы" or press2 == "s"):
            #    press2 = None
            #    add_v += 1
            #    print("added", time.time()-st)
            #    #1-375; 2-3

    elif (press == 'у' or press == 'e'):
        print("finishing", time.time()-st)
        break