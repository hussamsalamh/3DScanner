""""
TODO : need to find the distance from screen to can
also think if need to find the distance for reflected light
in case for smooth surface
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np

WHITE = 255
BLACK = 0


class ProcessFrame:
    def __init__(self, image):
        self.image = image
        self.findStraightLine()
        self.displacement = self.calculateDisplacement()
        self.slope = self.calculateSlope()
        self.upperMark = None
        self.bottomMark = None
        self.angle = 0

    """
    clean the image -> apply the threshold
    """

    def processImage(self):
        "only mask the green and display it "
        img = cv2.imread(self.image)
        gimg = img.copy()[:, :, 1]
        gimg[gimg < 220] = BLACK
        gimg[gimg > 0] = WHITE

    """
    find the beginning of the line and move the matrix 
    after that return an array that describe 
    for each element in row it will show you 
    the distance from the straight line
    
    """

    def findStraightLine(self):
        self.processImage()
        pass

    def calculateDisplacement(self) -> list:
        pass

    "calculate slope for each pixel "

    def calculateSlope(self) -> list:
        pass

    def alignScreen(self):
        """self.image now its 2d bc threshold"""
        pass

    def calculate_angle(self, img, x_bars):
        # to calculate the angle
        bar_1 = x_bars[0]
        bar_2 = x_bars[~0]
        y_offset = abs(bar_1[0] - bar_2[1])

        y1 = int((bar_1[0] + bar_1[1]) / 2)
        x1 = 0
        for x1 in range(img.shape[1]):
            if img[y1, x1] == 0:
                break
        y2 = int((bar_2[0] + bar_2[1]) / 2)
        x2 = 0
        for x2 in range(img.shape[1]):
            if img[y2, x2] == 0:
                break
        t = np.arctan(abs(x1 - x2) / y_offset)
        t_deg = np.degrees(t)
        self.angle = t_deg
        # print(f'Image is rotated by {t_deg} degrees')
        return t_deg

    def rotate_image(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        if image.ndim == 3:
            fill = (WHITE, WHITE, WHITE)
        else:
            fill = WHITE
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=fill)
        return result


def get_min_xy(img):
    """
    find the min x and max y in
    :param img: numpy matrix of image
    :return: find where the bars start
    """
    min_x, max_y = 0, 0
    for x in range(img.shape[1]):
        if np.any(img[:, x] == BLACK):
            min_x = x
            break
    for y in range(img.shape[0] - 1, 0, -1):
        if np.any(img[y, :] == BLACK):
            max_y = y
            break
    return min_x, max_y


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


path = "C:\\Users\\Hussam Salamh\\Desktop\\3DScanner\\tmp.jpg"
a = ProcessFrame(path)
