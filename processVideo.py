"""
This class will return a matrix where each element
will present the derivative from boundry to the point in the matrix

this will return a matrix which all the element present the dritive

"""
import time

from processFrame import *


class ProcessVideo:
    def __init__(self, path, freq, x, y):
        # path of videos
        self.x = x
        self.y = y
        self.freq = freq
        self.path = path
        self.derivativeMatrix = None
        self.relationShip = None

    def divideVideo(self):
        capture = cv2.VideoCapture(self.path)
        frameNumber = 1
        while True:
            startTime = time.time()
            success, frame = capture.read()
            processFrame = ProcessFrame(frame, self.freq, startTime - time.time(), self.x, self.y)
            self.derivativeMatrix = np.c_[self.derivativeMatrix, processFrame.dy.T]
            if frameNumber == 1:
                self.relationShip = processFrame.relationShip
            if not success:
                break
