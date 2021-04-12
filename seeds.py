from os.path import isfile, join
from os import listdir
import numpy as np
import cv2 as cv
window_capture_name, window_detection_name = 'Video Capture', 'Object Detection'
window_detection_name = "frame"

imagesPath = "Images/"
onlyfiles = [f for f in listdir(imagesPath) if isfile(join(imagesPath, f))]

class SeedSeggregator:
    def __init__(self) -> None:
        self.paused = False
        self.kernel = np.ones((4, 4), 'int')
        self.percentages = {}
        self.f = open("out.txt", "w+")

    def __showVid(self, refno, frame, title=""):
        refno -= 1
        if title == "":
            title = str(refno)
        cv.imshow(title, frame)
        cv.moveWindow(title, (refno % 3)*600, (refno//3)*600)

    def __calcPercentage(self, msk):
        ''' 
        returns the percentage of white in a binary image 
        '''
        height, width = msk.shape[:2]
        num_pixels = height * width
        count_white = cv.countNonZero(msk)
        percent_white = (count_white/num_pixels) * 100
        percent_white = round(percent_white, 2)
        return percent_white

    def __applyHSVThreshold(self, frame, threshold):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(
            hsv, (threshold[0], threshold[1], threshold[2]), (threshold[3], threshold[4], threshold[5]))
        dialatedMask = cv.dilate(mask, self.kernel)
        maskedFrame = cv.bitwise_and(
            frame, frame, mask=dialatedMask)
        return dialatedMask, maskedFrame

    def processFiles(self):
        for image in onlyfiles:
            imgx = cv.imread(imagesPath + image)
            if not self.paused:
                frame = imgx
            frame = frame[50:-150, 50:-100]  # crop
            # frame = cv.resize(frame, (600, 600), interpolation=cv.INTER_AREA)  # resize
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            maskSeedsGroup = cv.inRange(hsv, (0, 0, 0), (179, 255, 243))
            # erosion = cv.erode(mask, kernel)
            dilatedMaskSeedsGroup = cv.dilate(maskSeedsGroup, self.kernel)
            # res = cv.bitwise_and(frame, frame, mask=mask)
            onlySeedsGroup = cv.bitwise_and(
                frame, frame, mask=dilatedMaskSeedsGroup)
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

            blueMask, blueFrame = self.__applyHSVThreshold(
                frame, [0, 0, 0, 180, 98, 150])
            yellowMask, yellowFrame = self.__applyHSVThreshold(
                frame, [0, 102, 60, 62, 255, 255])
            greenMask, greenFrame = self.__applyHSVThreshold(
                frame, [27, 0, 0, 84, 107, 184])
            self.f.write(image + "\n")
            self.f.write(
                "blue:"+str(self.__calcPercentage(blueMask))+"%,")
            self.f.write(
                "green:"+str(self.__calcPercentage(greenMask))+"%,")
            self.f.write(
                "yellow:"+str(self.__calcPercentage(yellowMask))+"%\n\n")
            # print("blue", calcPercentage(blueDilatedMaskSeedsGroup))
            # print("green", calcPercentage(greenDilatedMaskSeedsGroup))
            # print("yellow", calcPercentage(yellowDilatedMaskSeedsGroup))
            # showVid(4, blueSeedsGroup, 'blueSeedsGroup')
            # showVid(5, yellowSeedsGroup, 'yellowSeedsGroup')
            # showVid(6, greenSeedsGroup, 'greenSeedsGroup')
            self.__showVid(1, frame, "frame")
            self.__showVid(3, yellowFrame, 'onlySeedsGroupyellow')
            self.__showVid(4, greenFrame, 'onlySeedsGroupgreen')
            self.__showVid(5, blueFrame, 'onlySeedsGroupblue')

            key = cv.waitKey(1000) & 0xFF
            if key == ord("q"):
                break
            if key == ord(" "):
                paused = False if paused else True

        cv.destroyAllWindows()


seedSeggregator = SeedSeggregator()
seedSeggregator.processFiles()
