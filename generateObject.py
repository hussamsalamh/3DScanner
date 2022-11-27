"""
This class will generate the object
from here we can
"""
import matplotlib.pyplot as plt

from processVideo import *

NUMBER_OF_POINT_IN_PIXEL = 100


class Surface:
    def __init__(self, x, y, dy, dx, relationShip):
        self.x = np.linspace(x, x + relationShip, NUMBER_OF_POINT_IN_PIXEL)
        self.y = np.linspace(y, y + relationShip, NUMBER_OF_POINT_IN_PIXEL)
        self.x, self.y = np.meshgrid(self.x, self.y)
        self.yAngle = np.arctan(dy / relationShip / 2)
        self.xAngle = np.arctan(dx / relationShip / 2)
        self.z = np.zeros((self.x.shape[0], self.x.shape[1]))
        self.findZ()

    def findZ(self):
        t = np.transpose(np.array([self.x, self.y, self.z]), (1, 2, 0))

        m = [[np.cos(self.yAngle), 0, np.sin(self.xAngle)], [0, 1, 0],
             [-np.sin(self.xAngle), 0, np.cos(self.yAngle)]]

        self.x, self.y, self.z = np.transpose(np.dot(t, m), (2, 0, 1))

    def toVector(self):
        return np.array([self.x, self.y, self.z])


class GenerateObject:
    def __init__(self, path1, path2, x, y, freq):
        self.path1 = path1
        self.path2 = path2
        self.distanceLight = x
        self.distanceOfSurface = y
        self.freq = freq
        self.x = None
        self.y = None
        self.z = None
        self.relationShip = None

    def processVideo(self):
        firstVideo = ProcessVideo(self.path1, self.freq, self.distanceLight, self.distanceOfSurface)
        secondVideo = ProcessVideo(self.path2, self.freq, self.distanceLight, self.distanceOfSurface)
        if firstVideo.derivativeMatrix.shape != secondVideo.derivativeMatrix.shape:
            raise "Size of first and second video are not the same "
        for i in range(firstVideo.derivativeMatrix.shape[0]):
            x, y, z = None, None, None
            for j in range(firstVideo.derivativeMatrix.shape[1]):
                if i == 0 and j == 0:
                    self.relationShip = firstVideo.relationShip
                surface = Surface(i * self.relationShip, j * self.relationShip, firstVideo[i, j],
                                  secondVideo[i, j], self.relationShip)
                if i == 0:
                    x = np.copy(surface.x)
                    y = np.copy(surface.y)
                    z = np.copy(surface.z)
                x = np.vstack((x, surface.x))
                y = np.vstack((y, surface.y))
                z = np.vstack((z, surface.z))
            if self.x == None:
                self.x = np.copy(x)
                self.y = np.copy(y)
                self.z = np.copy(z)
            else:
                self.x = np.hstack((self.x, x))
                self.y = np.hstack((self.y, y))
                self.z = np.hstack((self.z, z))

    def displayObject(self):
        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.plot_surface(self.x, self.y, self.z)
        plt.show()
