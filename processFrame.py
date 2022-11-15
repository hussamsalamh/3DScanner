""""
TODO : need to find the distance from screen to can
also think if need to find the distance for reflected light
in case for smooth surface
"""


class ProcessFrame:
    def __init__(self, image):
        self.image = image
        self.findStraightLine()
        self.displacement = self.calculateDisplacement()
        self.slope = self.calculateSlope()

    """
    clean the image -> apply the threshold
    """

    def processImage(self):
        pass

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
