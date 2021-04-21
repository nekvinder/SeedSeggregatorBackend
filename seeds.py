from os.path import isfile, join
from os import listdir
import numpy as np
import cv2 as cv
import sys
import json


class SeedSeggregator:
    def __init__(self) -> None:
        self.__paused = False
        self.__kernel = np.ones((4, 4), 'int')
        self.__percentages = {}
        self.f = open("out.txt", "w+")
        self.__size = 250
        self.__marginX = 150
        self.__marginY = 150
        self.__debugging = False
        self.__segregatorConfig = {"yellow": [0, 102, 60, 62, 255, 255],
                                   "green": [27, 0, 0, 84, 107, 184]}

    def enableDebugging(self, ):
        self.__debugging = True

    def __showVid(self, refno, frame, title=""):
        refno -= 1
        if title == "":
            title = str(refno)
        frame = cv.resize(frame, (self.__size, self.__size),
                          interpolation=cv.INTER_AREA)  # resize
        cv.imshow(title, frame)
        cv.moveWindow(title, (refno % 3)*(self.__size + self.__marginX),
                      (refno//3)*(self.__size+self.__marginY))

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
        dialatedMask = cv.dilate(mask, self.__kernel)
        maskedFrame = cv.bitwise_and(
            frame, frame, mask=dialatedMask)
        return dialatedMask, maskedFrame

    def processImage(self, imagePath):
        imgx = cv.imread(imagePath)
        if not self.__paused:
            frame = imgx
        # frame = frame[50:-150, 50:-100]  # crop
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        maskSeedsGroup = cv.inRange(hsv, (0, 0, 0), (179, 255, 243))
        dilatedMaskSeedsGroup = cv.dilate(maskSeedsGroup, self.__kernel)
        onlySeedsGroup = cv.bitwise_and(
            frame, frame, mask=dilatedMaskSeedsGroup)
        ret, thrshed = cv.threshold(cv.cvtColor(
            onlySeedsGroup, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)
        contours, hier = cv.findContours(
            thrshed, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            for c in contours:
                areaTmp = cv.contourArea(c)
                if areaTmp > 500:
                    x, y, w, h = cv.boundingRect(c)
                    cv.putText(frame, str(areaTmp), (x, y),
                               cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
                    cv.rectangle(onlySeedsGroup, (x, y),
                                 (x+w, y+h), (255, 255, 0), 5)

        frame = frame[y: y+h, x:x+w]
        onlySeedsGroup = onlySeedsGroup[y: y+h, x:x+w]
        thrshed = thrshed[y: y+h, x:x+w]

        Masks = {}
        Frames = {}
        Percentages = {}

        for k in self.__segregatorConfig:
            Masks[k], Frames[k] = self.__applyHSVThreshold(
                frame, self.__segregatorConfig[k])
            Percentages[k] = self.__calcPercentage(Masks[k])

        if self.__debugging:
            self.__showVid(1, frame, "frame")
            i = 2
            for k in self.__segregatorConfig:
                self.__showVid(i, Frames[k], k)
                i += 1

        cv.waitKey(0) & 0xFF
        cv.destroyAllWindows()
        return Percentages


# print(sys.argv[1])
seedSeggregator = SeedSeggregator()
seedSeggregator.enableDebugging()

print(json.dumps(
    {"imageName": sys.argv[1], "percentages":  seedSeggregator.processImage(sys.argv[1])}))

# imagesPath = "Images/"
# onlyfiles = [f for f in listdir(imagesPath) if isfile(join(imagesPath, f))]
# for img in onlyfiles:
#     print({"imageName:": img, "percentages":  seedSeggregator.processImage(imagesPath+img)})
