#aqui vamos a hacer el intento de una piramide 
#el codigo fue extraido de
#https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution
#y esto salio con magia negra

from mathfunc import sub, dot, length, mul, norm, sum, V3, cross
from intersect import Intersect

class Pyramid(object):
  def __init__(self, center, direction, vertices= V3(0,0,0), material):
    self.center = center
    self.direction = direction
    self.vertices = vertices
    self.material = material

  def ray_intersect(self, orig, direction):
    N = sub(self.center, orig)
    D = dot(N, self.vertices[0])
    t = - (dot(N, orig) + D) / dot(N, direction)
    phit = orig + t * direction

    #compute planes normal
    a = sub(self.vertices[1], self.vertices[0])
    b = sub(self.vertices[2], self.vertices[0])

    #paso 1: encontrar P
    P = dot(N,  direction)
    if (abs(P) < 0.000000001):
      return False

    d = dot(N,  direction)

    

