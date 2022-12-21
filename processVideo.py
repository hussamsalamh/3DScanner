"""
This class will return a matrix where each element
will present the derivative from boundry to the point in the matrix

this will return a matrix which all the element present the dritive

"""
import numpy as np

from processFrame import *
BEGIN = 5
STOP = 20

class ProcessVideo:
    def __init__(self, path, x, y, direction):
        # path of videos
        self.x = x
        self.y = y
        self.path = path
        self.angles = None
        self.relationShip = None
        self.direction = direction
        if direction:
            self.rightToLeft()
        else:
            self.upToBottom()

    def upToBottom(self):
        capture = cv2.VideoCapture(self.path)
        frameNumber = 1
        while True:
            success, frame = capture.read()
            if frameNumber < BEGIN:
                frameNumber += 1
                continue
            if not success or frame is None or frameNumber == STOP:  # todo delete
                break
            processFrame = ProcessFrame(frame, self.x, self.y)
            if frameNumber == BEGIN:
                self.relationShip = processFrame.relationShip
                self.angles = processFrame.angles
            else:
                self.angles = np.vstack((self.angles, processFrame.angles))
            frameNumber += 1

    def rightToLeft(self):
        capture = cv2.VideoCapture(self.path)
        frameNumber = 1
        while True:
            success, frame = capture.read()
            if frameNumber < BEGIN:
                frameNumber += 1
                continue
            if not success or frame is None or frameNumber == STOP:  # todo delete
                break
            processFrame = ProcessFrame(frame, self.x, self.y)
            if frameNumber == BEGIN:
                self.relationShip = processFrame.relationShip
                self.angles = processFrame.angles.reshape(-1, 1)
            else:
                self.angles = np.c_[self.angles, processFrame.angles.reshape(-1, 1)]
            frameNumber += 1
