import cv2
from processFrame import *
from generateObject import *


class ProcessVideo:
    def __init__(self, path):
        # path of videos
        self.path = path
        self.object = GenerateObject()

    def divideVideo(self):
        capture = cv2.VideoCapture(self.path)
        frameNumber = 0
        while True:
            success, frame = capture.read()
            if not success:
                break
            # array where the light hit the screen
            self.object.slopes = ProcessFrame(frame).slope
            self.object.generatePoint(frameNumber)
