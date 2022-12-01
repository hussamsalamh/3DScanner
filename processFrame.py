""""

Need to enlarge the first line in order to not getting so much error in aligneFunction


w : we can find it from dt * fre < step-motor >
therefore we can find alpha

"""
import math

import cv2
import numpy as np

""" Image parameters """
WHITE = 255
BLACK = 0
GREEN = 160
" Numbers of marks in paper "
NUMBER_OF_MARK = 3
A4_PAPER = 297
""" approxmate pixel number from align the frame"""
STD_ALIGN = 100
STD_ALIGN_BOTTOM = 50
STD_PIXEL = 3
STD_RANGE = 15
STD_STRAIGHT_LINE = 3
''' Finding the relationship '''
DISTANCE_BETWEEN_MARK = A4_PAPER / (NUMBER_OF_MARK + 1)


class ProcessFrame:
    def __init__(self, image, frequency, time, x, y, frameNumber):
        self.frequency = frequency
        self.frameNumer = frameNumber
        self.x = x
        self.y = y
        self.initialAngle = 0
        self.time = time
        self.relationShip = 0
        self.image = image
        self.alpha = 0
        self.range = 0
        self.upperEnd = 0
        self.bottomBegin = 0
        self.straightLine = 0
        self.displacement = None  # Done
        self.angles = None  # in progress
        self.callFunction(image)  # Done

    """
    clean the image -> apply the threshold
    """

    def callFunction(self, image):
        if not isinstance(image, np.ndarray):
            self.image = cv2.imread(image)
        self.alignScreen()  # Done
        self.findStraightLine()  # Done
        self.findCoord()
        self.relationShip = DISTANCE_BETWEEN_MARK / self.range
        self.calculateDisplacement()
        self.angles = self.findAlpha()

    def findCoord(self):
        for i in range(self.image.shape[0] - STD_ALIGN):
            if self.image[STD_ALIGN + i, self.straightLine] != WHITE:
                self.upperEnd = i + STD_ALIGN
                break
        for j in range(self.image.shape[0]):
            if self.image[self.image.shape[0] - STD_ALIGN - j, self.straightLine] != WHITE:
                self.bottomBegin = self.image.shape[0] - STD_ALIGN - j
                break

    def appleThreshold(self):
        """only mask the green and display it """
        self.image = self.image.copy()[:, :, 1]
        self.image[self.image < GREEN] = BLACK
        self.image[self.image > 0] = WHITE

    """
    find the beginning of the line and move the matrix 
    after that return an array that describe 
    for each element in row it will show you 
    the distance from the straight line
    
    """

    def findMean(self, row, index, color=WHITE, limit=STD_RANGE):
        interVail = STD_PIXEL
        count = 0
        for i in range(limit):
            if self.image[row, index + i] < color:
                if interVail == 0:
                    return index + count // 2
                else:
                    interVail -= 1
            else:
                count += 1
                interVail = STD_PIXEL
        return index

    def findStraightLine(self):
        stillWhite = False
        count = 0
        for i in range(self.image.shape[1]):
            if count == 1:
                self.range += 1
            if self.image[STD_ALIGN, i] == WHITE and not stillWhite:
                count += 1
                stillWhite = True
                if NUMBER_OF_MARK // 2 + 1 == count:
                    self.straightLine = self.findMean(STD_ALIGN, i)
                    return
            if self.image[STD_ALIGN, i] == BLACK and stillWhite:
                stillWhite = False

    def calculateDisplacementHelper(self, y):
        for i in range(self.straightLine - self.range // 2,
                       self.straightLine + self.range // 2):
            if self.image[y, i] >= GREEN:
                return self.findMean(y, i, GREEN) - self.straightLine
        return 0

    def calculateDisplacement(self):
        self.displacement = np.zeros(self.image.shape[0])
        for y in range(self.upperEnd + 1, self.bottomBegin):
            self.displacement[y] = self.calculateDisplacementHelper(y) * self.relationShip

    "calculate slope for each pixel "

    def findAlpha(self):
        return -np.arctan(self.y / (self.x + self.displacement)) + np.arctan(self.y / self.x)

    def alignScreen(self):
        """self.image now its 2d bc threshold"""
        if self.image.shape[0] > self.image.shape[1]:
            self.image = cv2.rotate(self.image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.appleThreshold()
        self.rotateImage()

    def rotateImage(self):
        if self.image.ndim == 3:
            fill = (BLACK, BLACK, BLACK)
        else:
            fill = BLACK
        dx = getDistance(self.image)
        angle = calculateAngle(dx, self.image.shape[0])
        center = tuple(np.array(self.image.shape[1::-1]) / 2)
        rotMatrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.image = cv2.warpAffine(self.image, rotMatrix, self.image.shape[1::-1], flags=cv2.INTER_LINEAR,
                                    borderValue=fill)


def calculateAngle(dx, y):
    # to calculate the angle
    t = np.arctan(dx / y)
    t_deg = np.degrees(t)
    # print(f'Image is rotated by {t_deg} degrees')
    return t_deg


def getDistance(img):
    """
    find the min x and max y in
    :param img: numpy matrix of image
    :return: find where the bars start
    """
    x1, x2 = 0, 0
    for x in range(img.shape[1]):
        if np.any(img[STD_ALIGN, x] == WHITE):
            x1 = x
            break
    for y in range(img.shape[1]):
        if np.any(img[img.shape[0] - STD_ALIGN_BOTTOM, y] == WHITE):
            x2 = y
            break
    return abs(x1 - x2)

# path = "C:\\Users\\Hussam Salamh\\Desktop\\3DScanner\\rot.png"
# a = ProcessFrame(path)
