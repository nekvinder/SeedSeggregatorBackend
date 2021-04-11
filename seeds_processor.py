import numpy as np
import cv2 as cv
window_capture_name, window_detection_name = 'Video Capture', 'Object Detection'
window_detection_name = "frame"
paused = False
imgx = cv.imread('Images/DSC_0078.JPG')


def showVid(refno, frame, title=""):
    refno -= 1
    if title == "":
        title = str(refno)
    cv.imshow(title, frame)
    cv.moveWindow(title, (refno % 3)*600, (refno//3)*600)


def calcPercentage(msk):
    ''' 
    returns the percentage of white in a binary image 
    '''
    height, width = msk.shape[:2]
    num_pixels = height * width
    count_white = cv.countNonZero(msk)
    percent_white = (count_white/num_pixels) * 100
    percent_white = round(percent_white, 2)
    return percent_white


kernel = np.ones((4, 4), 'int')
while True:
    if not paused:
        frame = imgx
    frame = frame[50:-150, 50:-100]  # crop
    # frame = cv.resize(frame, (600, 600), interpolation=cv.INTER_AREA)  # resize
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskSeedsGroup = cv.inRange(hsv, (0, 0, 0), (179, 255, 243))
    # erosion = cv.erode(mask, kernel)
    dilatedMaskSeedsGroup = cv.dilate(maskSeedsGroup, kernel)
    # res = cv.bitwise_and(frame, frame, mask=mask)
    onlySeedsGroup = cv.bitwise_and(frame, frame, mask=dilatedMaskSeedsGroup)
    ret, thrshed = cv.threshold(cv.cvtColor(
        onlySeedsGroup, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)
    contours, hier = cv.findContours(
        thrshed, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        for c in contours:
            areaTmp = cv.contourArea(c)
            if areaTmp > 4000:
                x, y, w, h = cv.boundingRect(c)
                cv.putText(frame, str(areaTmp), (x, y),
                           cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
                cv.rectangle(onlySeedsGroup, (x, y),
                             (x+w, y+h), (255, 255, 0), 5)

    frame = frame[y: y+h, x:x+w]  # crop
    onlySeedsGroup = onlySeedsGroup[y: y+h, x:x+w]  # crop
    thrshed = thrshed[y: y+h, x:x+w]  # crop
    # print("onlySeedsPixel", calcPercentage(maskSeedsGroup))

    # cv.putText(frame, str(pauseMS), (0, 10),
    #            cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    # showVid(3, mask, "mask")
    # showVid(2, dilated, "dilated")
    # showVid(6, thrshed, 'thrshed')

    # Blue seeds filter
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskSeedsGroup = cv.inRange(hsv, (0, 0, 0), (180, 98, 150))
    blueDilatedMaskSeedsGroup = cv.dilate(maskSeedsGroup, kernel)
    blueSeedsGroup = cv.bitwise_and(
        frame, frame, mask=blueDilatedMaskSeedsGroup)
    ret, thrshed = cv.threshold(cv.cvtColor(
        blueSeedsGroup, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)

    # Yellow seeds filter
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskSeedsGroup = cv.inRange(hsv, (0, 102, 60), (62, 255, 255))
    yellowDilatedMaskSeedsGroup = cv.dilate(maskSeedsGroup, kernel)
    yellowSeedsGroup = cv.bitwise_and(
        frame, frame, mask=yellowDilatedMaskSeedsGroup)
    ret, thrshed = cv.threshold(cv.cvtColor(
        yellowSeedsGroup, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)

    # Green seeds filter
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskSeedsGroup = cv.inRange(hsv, (27, 0, 0), (84, 107, 184))
    greenDilatedMaskSeedsGroup = cv.dilate(maskSeedsGroup, kernel)
    greenSeedsGroup = cv.bitwise_and(
        frame, frame, mask=greenDilatedMaskSeedsGroup)
    ret, thrshed = cv.threshold(cv.cvtColor(
        greenSeedsGroup, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)

    print("blue", calcPercentage(blueDilatedMaskSeedsGroup))
    print("green", calcPercentage(greenDilatedMaskSeedsGroup))
    print("yellow", calcPercentage(yellowDilatedMaskSeedsGroup))
    showVid(4, blueSeedsGroup, 'blueSeedsGroup')
    showVid(5, yellowSeedsGroup, 'yellowSeedsGroup')
    showVid(6, greenSeedsGroup, 'greenSeedsGroup')
    showVid(2, onlySeedsGroup, 'onlySeedsGroup')
    showVid(1, frame, "frame")

    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord(" "):
        paused = False if paused else True

cv.destroyAllWindows()
