"""
This class will generate the object
from here we can
"""
import matplotlib.pyplot as plt
from processFolder import *

NUMBER_OF_POINT_IN_PIXEL = 20

INTER_VAIL = 10     # TODO need to change that


class Surface:
    def __init__(self, x, y, angleX, angleY, relationShip):
        self.angleX = angleX
        self.angleY = angleY
        self.xAdd = x
        self.yAdd = y
        self.relationShip = relationShip
        self.x = np.linspace(0, relationShip, NUMBER_OF_POINT_IN_PIXEL)
        self.y = np.linspace(0, relationShip, NUMBER_OF_POINT_IN_PIXEL)
        self.x, self.y = np.meshgrid(self.x, self.y)
        self.z = np.zeros((self.x.shape[0], self.x.shape[1]))
        self.findZ()

    def findZ(self):
        t = np.transpose(np.array([self.x, self.y, self.z]), (1, 2, 0))

        m = [[np.cos(self.angleY), 0, np.sin(self.angleX)], [0, 1, 0],
             [-np.sin(self.angleX), 0, np.cos(self.angleY)]]

        self.x, self.y, self.z = np.transpose(np.dot(t, m), (2, 0, 1))
        self.x += self.xAdd * self.relationShip
        self.y += self.yAdd * self.relationShip

    def toVector(self):
        return np.array([self.x, self.y, self.z])





class GenerateObject:
    def __init__(self, path1, path2, x, y):
        self.path1 = path1
        self.path2 = path2
        self.distanceLight = x
        self.distanceOfSurface = y
        self.x = None
        self.y = None
        self.z = None
        self.relationShip = None
        self.displayObject()

    def generateObject(self):
        processVideos = ProcessFolder(self.path1, self.path2, self.distanceLight, self.distanceOfSurface)
        # if firstVideo.angles.shape != secondVideo.angles.shape:
        #     raise "Size of first and second video are not the same "
        verticalAngle = processVideos.angleVertical
        horizontalAngle = processVideos.angleHorizontal
        self.relationShip = processVideos.relationshipVertical
        for i in range(INTER_VAIL):  # TODO : need to change it to len
            x, y, z = None, None, None
            for j in range(INTER_VAIL):  # TODO : need to change it to len
                surface = Surface(i * self.relationShip, j * self.relationShip, verticalAngle.angles[i, j],
                                  horizontalAngle.angles[i, j], self.relationShip)
                if j == 0:
                    x = np.copy(surface.x)
                    y = np.copy(surface.y)
                    z = np.copy(surface.z)
                else:
                    x = np.vstack((x, surface.x))
                    y = np.vstack((y, surface.y))
                    z = np.vstack((z, surface.z))
            if self.x is None:
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


path1 = "C:\\Users\\Hussam Salamh\\Desktop\\3DScanner\\tmp2Video.avi"
path2 = "C:\\Users\\Hussam Salamh\\Desktop\\3DScanner\\tmp2Video.avi"

generate = GenerateObject(path1, path2, 1, 3, 30)
