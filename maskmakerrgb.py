import numpy as np
import cv2 as cv
import AGTCAM.ConfiManagerentry as config
vals = config.loadConfig()
max_value, max_value_H = 255, 255
low_V, low_H, low_S = 0, 0, 0
high_H, high_V, high_S = max_value_H, max_value, max_value
low_H, low_S, low_V, high_H, high_S, high_V = vals
window_capture_name, window_detection_name = 'Video Capture', 'Object Detection'
low_H_name, low_S_name, low_V_name = 'Low H', 'Low S', 'Low V'
high_H_name, high_S_name, high_V_name = 'High H', 'High S', 'High V'
pauseMS = 1


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


def showVid(refno, frame, title=""):
    refno -= 1
    if title == "":
        title = str(refno)
    cv.imshow(title, frame)
    cv.moveWindow(title, (refno % 3)*600, (refno//3)*600)


cap = config.loadCap()

window_detection_name = "frame"
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name, low_H,
                  max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name, high_H,
                  max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name, low_S,
                  max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name, high_S,
                  max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name, low_V,
                  max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name, high_V,
                  max_value, on_high_V_thresh_trackbar)

paused = False
while True:
    if not paused:
        _, frame = cap.read()
    if not _:
        break
    # frame=frame[10:-10,10:-10] #crop
    frame = cv.resize(frame, (600, 600), interpolation=cv.INTER_AREA)  # resize
    # hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame, (low_H, low_S, low_V), (high_H, high_S, high_V))

    kernel = np.ones((8, 8), 'int')
    erosion = cv.erode(mask, kernel)
    dilated = cv.dilate(mask, kernel)
    res = cv.bitwise_and(frame, frame, mask=dilated)
    ret, thrshed = cv.threshold(cv.cvtColor(
        res, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)
    contours, hier = cv.findContours(
        thrshed, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # approx = cv.approxPolyDP(contours, 0.02*cv.arcLength(contours, True), True)
    # x = approx.ravel()[0]
    # y = approx.ravel()[1]

    if len(contours) > 0:
        for c in contours:
            areaTmp = cv.contourArea(c)
            # if areaTmp > 4000 and areaTmp < 10000:
            if areaTmp > 4000:

                x, y, w, h = cv.boundingRect(c)
                cv.putText(frame, str(areaTmp), (x, y),
                           cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
                cv.rectangle(res, (x, y), (x+w, y+h), (255, 255, 0), 5)
            # print(areaTmp)
            # print("*"*55)

    cv.putText(frame, str(pauseMS), (0, 10),
               cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

    showVid(3, mask, "mask")
    # showVid(2, dilated, "dilated")
    showVid(5, res, 'res')
    showVid(6, thrshed, 'thrshed')
    showVid(1, frame, "frame")

    key = cv.waitKey(pauseMS) & 0xFF
    if key == ord("q"):
        break
    if key == ord("+"):
        pauseMS += 5
        print('+')
    if key == ord("-"):
        pauseMS -= 5
        print('-')
    if key == ord(" "):
        paused = False if paused else True
    if key == ord("p"):
        print("mask = cv.inRange(hsv,np.array([{}, {}, {}]), np.array([{}, {}, {}]))".format(
            low_H, low_S, low_V, high_H, high_S, high_V))
    if key == ord("s"):
        config.saveConfig(low_H, low_S, low_V, high_H, high_S, high_V)
        print('saved')
    if key == ord("r"):
        cv.setTrackbarPos(low_H_name, window_detection_name, 0)
        cv.setTrackbarPos(low_S_name, window_detection_name, 0)
        cv.setTrackbarPos(low_V_name, window_detection_name, 0)
        cv.setTrackbarPos(high_H_name, window_detection_name, max_value_H)
        cv.setTrackbarPos(high_S_name, window_detection_name, max_value)
        cv.setTrackbarPos(high_V_name, window_detection_name, max_value)
        print('reset')

cv.destroyAllWindows()
# if input("Y to save")=='y':
# config.saveConfig(low_H, low_S, low_V, high_H, high_S, high_V)
