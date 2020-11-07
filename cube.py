from plane import Plane
from mathfunc import sum, V3
from intersect import Intersect

class Cube(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        halfSize = size / 2

        self.planes.append( Plane( sum(position, V3(halfSize,0,0)), V3(1,0,0), material))
        self.planes.append( Plane( sum(position, V3(-halfSize,0,0)), V3(-1,0,0), material))

        self.planes.append( Plane( sum(position, V3(0,halfSize,0)), V3(0,1,0), material))
        self.planes.append( Plane( sum(position, V3(0,-halfSize,0)), V3(0,-1,0), material))

        self.planes.append( Plane( sum(position, V3(0,0,halfSize)), V3(0,0,1), material))
        self.planes.append( Plane( sum(position, V3(0,0,-halfSize)), V3(0,0,-1), material))


    def rayIntersect(self, orig, direction):

        epsilon = 0.001

        boundsMin = [0,0,0]
        boundsMax = [0,0,0]

        for i in range(3):
            boundsMin[i] = self.position[i] - (epsilon + self.size / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size / 2)

        t = float('inf')
        intersect = None

        for plane in self.planes:
            planeInter = plane.rayIntersect(orig, direction)

            if planeInter is not None:

                if planeInter.point[0] >= boundsMin[0] and planeInter.point[0] <= boundsMax[0]:
                    if planeInter.point[1] >= boundsMin[1] and planeInter.point[1] <= boundsMax[1]:
                        if planeInter.point[2] >= boundsMin[2] and planeInter.point[2] <= boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal)