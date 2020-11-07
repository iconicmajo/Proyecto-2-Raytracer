from plane import Plane
from mathfunc import sum, V3, sub, norm, cross, dot, mul, length, barycentric
from intersect import Intersect

class Pyramid(object):
    def __init__(self, arrVec, material):
        self.arrVec = arrVec
        self.material = material
        #print("aqui")

    def side(self, v0, v1, v2, origin, direction):
        v0v1 = sub(v1, v0)
        v0v2 = sub(v2, v0)

        N = mul(cross(v0v1, v0v2),1)
        # area2 = length(N)

        raydirection = dot(N, direction)

        if abs(raydirection) < 0.0001:
            return None
        
        d = dot(N, v0)
        #print('D', d)
        
        t = (dot(N, origin) + d)/raydirection
        
        #print('T', t)
        
        if t < 0:
            return None

        P = sum(origin, mul(direction, t))
        #P = V3(-1,1,0)
        U, V, W = barycentric(v0, v1, v2, P)
        #print(U, V, W)
        if U<0 or V<0 or W<0:
            return None
        else: 
            return Intersect(distance = d,
                         point = P,
                         normal = norm(N))
        #assert t<0, 'murio'
        
        

        edge0 = sub(v1, v0)
        vp0 = sub(P, v0)

        C = cross(edge0, vp0)

        nc = dot(N, C)
        #print("C", nc)
        if nc < 0:
            return None

        edge1 = sub(v2, v1)
        vp1 = sub(P, v1)

        C = cross(edge1, vp1)

        if dot(N, C) < 0:
            return None

        edge2 = sub(v0, v2)
        vp2 = sub(P, v2)

        C = cross(edge2, vp2)

        if dot(N, C) < 0:
            return None

        #print("hola")

        return Intersect(distance = (t / raydirection),
                         point = P,
                         normal = norm(N))


    def rayIntersect(self, origin, direction):
        v0, v1, v2, v3 = self.arrVec
        planes = [
        self.side(v0, v3, v2, origin, direction),
        self.side(v0, v1, v2, origin, direction),
        self.side(v1, v3, v2, origin, direction),
        self.side(v0, v1, v3, origin, direction)
        ]

        '''
        planes = [
        self.side(v0, v3, v2, origin, direction),
        self.side(v0, v1, v2, origin, direction),
        self.side(v1, v3, v2, origin, direction),
        self.side(v0, v1, v3, origin, direction)
        ]
        '''


        t = float('inf')
        intersect = None

        for plane in planes:
            #planeInter = plane.rayIntersect(orig, direction)
            if plane is not None:
                if plane.distance < t:
                    t = plane.distance
                    intersect = plane

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal)


        
