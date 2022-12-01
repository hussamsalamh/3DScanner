"""
This class will return a matrix where each element
will present the derivative from boundry to the point in the matrix

this will return a matrix which all the element present the dritive

"""
import time

import cv2

from processFrame import *


class ProcessVideo:
    def __init__(self, path, freq, x, y):
        # path of videos
        self.x = x
        self.y = y
        self.freq = freq
        self.path = path
        self.angles = None
        self.relationShip = None
        self.divideVideo()

    def divideVideo(self):
        capture = cv2.VideoCapture(self.path)
        fps = capture.get(cv2.CAP_PROP_FPS)
        timeStamps = [capture.get(cv2.CAP_PROP_POS_MSEC)]
        calc_timestamps = [0.0]
        frameNumber = 1
        while True:
            timeStamps[-1] = capture.get(cv2.CAP_PROP_POS_MSEC)
            calc_timestamps[-1] = calc_timestamps[-1] + 1000 / fps
            success, frame = capture.read()
            if frameNumber < 5:
                frameNumber += 1
                continue
            if not success or frame is None or frameNumber == 10:  # todo delete
                break
            processFrame = ProcessFrame(frame, self.freq, abs(timeStamps[-1] - calc_timestamps[-1]), self.x, self.y,
                                        frameNumber)
            if frameNumber == 5:
                self.relationShip = processFrame.relationShip
                self.angles = processFrame.angles
            else:
                self.angles = np.c_[self.angles, processFrame.angles.T]
            frameNumber += 1
