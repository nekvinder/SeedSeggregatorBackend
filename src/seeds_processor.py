import numpy as np
import cv2 as cv

max_value, max_value_H = 255, 360//2
low_V, low_H, low_S = 0, 0, 0
high_H, high_V, high_S = max_value_H, max_value, max_value
low_H, low_S, low_V, high_H, high_S, high_V = [0, 0, 0, 180, 255, 255]
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
imgx = cv.imread('/home/nekvinder/Desktop/color-picker-casual.png')

while True:
    if not paused:
        frame = imgx
    frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_AREA)  # resize
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, (low_H, low_S, low_V), (high_H, high_S, high_V))

    res = cv.bitwise_and(frame, frame, mask=mask)
    ret, thrshed = cv.threshold(cv.cvtColor(
        res, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)
    contours, hier = cv.findContours(
        thrshed, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    showVid(2, res, 'res')
    showVid(3, thrshed, 'thrshed')
    showVid(1, frame, "frame")

    key = cv.waitKey(pauseMS) & 0xFF
    if key == ord("q"):
        break
    if key == ord(" "):
        paused = False if paused else True
    if key == ord("p"):
        print("mask = cv.inRange(hsv,np.array([{}, {}, {}]), np.array([{}, {}, {}]))".format(
            low_H, low_S, low_V, high_H, high_S, high_V))
    if key == ord("s"):
        # config.saveConfig(low_H, low_S, low_V, high_H, high_S, high_V)
        print('couldnt saved')
    if key == ord("r"):
        cv.setTrackbarPos(low_H_name, window_detection_name, 0)
        cv.setTrackbarPos(low_S_name, window_detection_name, 0)
        cv.setTrackbarPos(low_V_name, window_detection_name, 0)
        cv.setTrackbarPos(high_H_name, window_detection_name, max_value_H)
        cv.setTrackbarPos(high_S_name, window_detection_name, max_value)
        cv.setTrackbarPos(high_V_name, window_detection_name, max_value)
        print('reset')

cv.destroyAllWindows()
