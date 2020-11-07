from mathfunc import sum, V3, dot, sub, norm, mul
from intersect import Intersect

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = norm(normal)
        self.material = material

    def rayIntersect(self, orig, dir):
        # t = (( position - origRayo) dot normal) / (dirRayo dot normal)

        denom = dot(dir, self.normal)

        if abs(denom) > 0.0001:
            t = dot(self.normal, sub(self.position, orig)) / denom
            if t > 0:
                # P = O + tD
                hit = sum(orig, mul(dir, t))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal)

        return None
