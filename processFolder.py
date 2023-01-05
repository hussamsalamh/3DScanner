"""

This class will take the folder image that has been generated from control.py
and send each image to process Frame in order to generate the angle array and send it to
generateObject.py

"""
import os

import numpy as np

from processFrame import ProcessFrame


def takeImage(path, array):
    for images in os.listdir(path):

        # check if the image ends with png or jpg or jpeg
        if (images.endswith(".png") or images.endswith(".jpg")
                or images.endswith(".jpeg")):
            array.append(images)


class ProcessFolder:
    def __init__(self, folder1, folder2, x, y):
        self.verticalScanPath = folder1
        self.horizontalScanPath = folder2
        self.verticalImage = []
        self.horizontalImage = []
        self.x = x
        self.y = y
        self.relationshipHorizontal = 0
        self.relationshipVertical = 0
        self.angleHorizontal = None
        self.angleVertical = None

    def findAngleHorizontal(self):
        np.sort(self.horizontalImage)
        for i in range(len(self.horizontalImage)):
            processFrame = ProcessFrame(self.horizontalImage[i], self.x, self.y)
            if i == 0:
                self.relationshipHorizontal = processFrame.relationShip
                self.angleHorizontal = processFrame.angles.reshape(-1, 1)
            else:
                self.angleHorizontal = np.c_[self.angleHorizontal, processFrame.angles.reshape(-1, 1)]

    def findAngleVertical(self):
        for i in range(len(self.verticalImage)):
            processFrame = ProcessFrame(self.verticalImage[i], self.x, self.y)
            if i == 0:
                self.relationshipVertical = processFrame.relationShip
                self.angleVertical = processFrame.angles
            else:
                self.angleVertical = np.vstack((self.angleVertical, processFrame.angles))
