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

    cv.createTrackbar("from_hight1", "Tracking1", 53, 200, nothing)
    cv.createTrackbar("to_hight1", "Tracking1", 545, 1440, nothing)

    cv.createTrackbar("from_hight2", "Tracking1", 53, 200, nothing)
    cv.createTrackbar("to_hight2", "Tracking1", 545, 1440, nothing)

    cv.createTrackbar("from_hight3", "Tracking1", 53, 200, nothing)
    cv.createTrackbar("to_hight3", "Tracking1", 545, 1440, nothing)

    cv.createTrackbar("from_hight4", "Tracking1", 53, 200, nothing)
    cv.createTrackbar("to_hight4", "Tracking1", 545, 1440, nothing)


    cv.createTrackbar("from_width", "Tracking1", 303, 900, nothing)
    cv.createTrackbar("to_width", "Tracking1", 580, 2560, nothing)

    #cv.createTrackbar("from hight", "Tracking", 43, 800, nothing)
    #cv.createTrackbar("to hight", "Tracking", 500, 1440, nothing) #724

    #cv.createTrackbar("from width", "Tracking", 40, 100, nothing)
    #cv.createTrackbar("to width", "Tracking", 60, 100, nothing)

    #cv.createTrackbar("from width2", "Tracking", 0, 100, nothing)
    #cv.createTrackbar("to width2", "Tracking", 20, 100, nothing)

    #cv.createTrackbar("from width3", "Tracking", 55, 100, nothing)
    #cv.createTrackbar("to width3", "Tracking", 75, 100, nothing)

    #cv.createTrackbar("from width4", "Tracking", 40, 100, nothing)
    #cv.createTrackbar("to width4", "Tracking", 60, 100, nothing)
    pass

def get_tr():
    top = [cv.getTrackbarPos(f"from_hight{i+1}", "Tracking1") for i in range(4)]
    height = [cv.getTrackbarPos(f"to_hight{i+1}", "Tracking1")-ftop[i] for i in range(4)]
    left = cv.getTrackbarPos("from_width", "Tracking1")
    width = cv.getTrackbarPos("to_width", "Tracking1")-fleft

    top = [top[0], top[1], top[2], top[3]]
    height = [height[0], height[1], height[2], height[3]]

    #top = [cv.getTrackbarPos("from hight", "Tracking"), cv.getTrackbarPos("from hight", "Tracking"),
    #       cv.getTrackbarPos("from hight", "Tracking"), cv.getTrackbarPos("from hight", "Tracking")]
    #height = cv.getTrackbarPos("to hight", "Tracking")-top[0]

    #left = [cv.getTrackbarPos("from width", "Tracking"), cv.getTrackbarPos("from width2", "Tracking"),
    #        cv.getTrackbarPos("from width3", "Tracking"), cv.getTrackbarPos("from width4", "Tracking")]
    #width = [cv.getTrackbarPos("to width", "Tracking"),
    #        cv.getTrackbarPos("to width2", "Tracking"),
    #        cv.getTrackbarPos("to width3", "Tracking"),
    #        cv.getTrackbarPos("to width4", "Tracking")]

    #top = [top[0], top[1]+25, top[2]+25, top[3]]
    #left = [left[0]+420, left[1]+520, left[2]+620, left[3]+720]
    #width = [width[0]+421-left[0], width[1]+521-left[1],
    #         width[2]+621-left[2], width[3]+721-left[3]]

    return  top, height, left, width #, ftop, fheight, fleft, fwidth

mou = 1
init_tr()
top, height, left, width = get_tr()
#print(top, height, left, width)
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
            top, height, left, width = get_tr()
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

            for i in range(4):
                img1 = np.array(sct.grab({'top': top[i], 'left': left[i], 'width': width[i], 'height': height}))
                # 'top': top, 'left': left, 'width': width, 'height': height
                #img1 = cv.imread("img.jpg")

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
                        cv.rectangle(img1, (x, y), (x + w, y + h), (0,255,0), 2)
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