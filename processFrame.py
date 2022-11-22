""""
Need to find the distance of x and y
dx = we can find it from findDistance function
dy = ( 2y * ( x + dx ) - 2xy ) / 2x
theta = arctan ( x/y )

alpha : angle from beginning of surface until the point

w : we can find it from dt * fre < step-motor >
therefore we can find alpha

"""
import cv2
import numpy as np

""" Image parameters """
WHITE = 255
BLACK = 0
GREEN = 220
" Numbers of marks in paper "
NUMBER_OF_MARK = 3
A4_PAPER = 297
""" approxmate pixel number from align the frame"""
STD_ALIGN = 15
STD_STRAIGHT_LINE = 3
''' Finding the relationship '''
DISTANCE_BETWEEN_MARK = A4_PAPER / (NUMBER_OF_MARK + 1)
DISTANCE_FROM_SCREEN = 1
HIGTH_FROM_SCREEN = 2


class ProcessFrame:
    def __init__(self, image, frequency, time, x):
        self.frequency = frequency
        self.origin = x
        self.time = time
        self.relationShip = 0
        self.firstFrame = True
        self.image = image
        self.alpha = 0
        self.range = 0
        self.straightLineCoordination = (0, 0)
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
        if self.firstFrame:
            self.findStraightLine()  # Done
        self.relationShip = DISTANCE_BETWEEN_MARK / self.range
        self.calculateDisplacement()
        self.angles = self.findAlpha()

    def appleThreshold(self):
        """only mask the green and display it """
        self.image = self.image.copy()[:, :, 1]
        self.image[self.image < 220] = BLACK
        self.image[self.image > 0] = WHITE

    """
    find the beginning of the line and move the matrix 
    after that return an array that describe 
    for each element in row it will show you 
    the distance from the straight line
    
    """

    def findStraightLine(self):
        self.firstFrame = False
        stillWhite = False
        count = 0
        for i in range(self.image.shape[1]):
            if count == 1:
                self.range += 1
            if self.image[STD_ALIGN, i] == WHITE and not stillWhite:
                count += 1
                stillWhite = True
                if NUMBER_OF_MARK // 2 + 1 == count:
                    self.straightLineCoordination = (i, 0)
                    break
            if self.image[STD_ALIGN, i] == BLACK and stillWhite:
                stillWhite = False

    def calculateDisplacementHelper(self, y):
        for i in range(self.straightLineCoordination[0] - self.range // 2,
                       self.straightLineCoordination[0] + self.range // 2):
            if self.image[y, i] > GREEN:
                return i - self.straightLineCoordination[0]
        return 0

    def calculateDisplacement(self):
        self.displacement = np.zeros(self.image.shape[0])
        for y in range(STD_STRAIGHT_LINE, self.image.shape[0]):
            self.displacement[y] = self.calculateDisplacementHelper(y) * self.relationShip

    "calculate slope for each pixel "

    @np.vectorize
    def findAlpha(self):
        dy = DISTANCE_FROM_SCREEN * (
                self.origin + self.displacement) / self.origin - DISTANCE_FROM_SCREEN / self.origin
        distanceFromBegin = self.frequency * self.time
        return np.arctan(dy / distanceFromBegin)

    def alignScreen(self):
        """self.image now its 2d bc threshold"""
        if self.image.shape[0] > self.image.shape[1]:
            self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
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
        if np.any(img[img.shape[0] - STD_ALIGN, y] == WHITE):
            x2 = y
            break
    return abs(x1 - x2)


def list_bars(img):
    black = False
    y_idx = []
    for y in range(img.shape[0]):
        if img[y, 0] == BLACK and not black:
            y_idx.append(y)
            black = True
        elif img[y, 0] > BLACK and black:
            y_idx.append(y - 1)
            black = False

    yy_idx = []
    for i in range(0, len(y_idx), 2):
        yy_idx.append((y_idx[i], y_idx[i + 1]))

    x_idx = []
    black = False
    for x in range(img.shape[1]):
        if img[-1, x] == 0 and not black:
            x_idx.append(x)
        elif img[-1, x] > 0 and black:
            x_idx.append(x - 1)

    xx_idx = []
    for i in range(0, len(x_idx), 2):
        xx_idx.append((x_idx[i], x_idx[i + 1]))
    return yy_idx, xx_idx


path = "C:\\Users\\Hussam Salamh\\Desktop\\3DScanner\\rot.png"
a = ProcessFrame(path)
