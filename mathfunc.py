#Maria Jose Castro Lemus 
#181202
#Graficas por Computadora - 10
#RT1: Esferas
#snowman


import struct 
from collections import namedtuple

class V3(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self):
    return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

class V2(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __repr__(self):
    return "V2(%s, %s)" % (self.x, self.y)

#V2 = namedtuple('Vertex2', ['x', 'y'])
#V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

class color(object):
    def __init__(self, r,g,b):
        self.r = r
        self.g = g 
        self.b = b

    def __add__(self, otherColor):
        r = self.r + otherColor.r
        g = self.g + otherColor.g
        b = self.b + otherColor.b

        return color(r, g, b)


    def __mul__(self, otherColor):
        r = self.r * otherColor
        g = self.g * otherColor
        b = self.b * otherColor

        return color(r, g, b)

    def __repr__(self):
        return "color (%s, %s, %s)" % (self.r, self.g, self.b)

    def toBytes(self):
        self.r = int(max(min(self.r, 255), 0))
        self.g = int(max(min(self.g, 255), 0))
        self.b = int(max(min(self.b, 255), 0))
        return bytes([self.b, self.g, self.r])
    
    __rmul__ = __mul__

def MM(a,b):
    c = []
    for i in range(0,len(a)):
        temp=[]
        for j in range(0,len(b[0])):
            s = 0
            for k in range(0,len(a[0])):
                s += a[i][k]*b[k][j]
            temp.append(s)
        c.append(temp)
    return c

def char(c):
    return struct.pack('=c', c.encode('ascii'))
def word(c):
    return struct.pack('=h', c)
def dword(c):
    return struct.pack('=l', c)
#def color(r, g, b):
#    return bytes([b, g, r])

def sum(v0, v1):
    """
      Input: 2 size 3 vectors
      Output: Size 3 vector with the per element sum
    """
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)


def sub(v0, v1):
    """
      Input: 2 size 3 vectors
      Output: Size 3 vector with the per element substraction
    """
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
    """
      Input: 2 size 3 vectors
      Output: Size 3 vector with the per element multiplication
    """
    return V3(v0.x * k, v0.y * k, v0.z * k)


def dot(v0, v1):
    """
      Input: 2 size 3 vectors
      Output: Scalar with the dot product
    """
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def length(v0):
    """
      Input: 1 size 3 vector
      Output: Scalar with the length of the vector
    """
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5


def norm(v0):
    """
      Input: 1 size 3 vector
      Output: Size 3 vector with the normal of the vector
    """
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)


def cross(u, w):
    # print(u, w)
    return V3(
        u.y * w.z - u.z * w.y,
        u.z * w.x - u.x * w.z,
        u.x * w.y - u.y * w.x,
    )


def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]
    xs.sort()
    ys.sort()

    xMin = round(xs[0])
    xMax = round(xs[-1])
    yMin = round(ys[0])
    yMax = round(ys[-1])

    return xMin, xMax, yMin, yMax


def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    if abs(cz) < 1:
        return -1, -1, -1

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz
    
    return  w, v, u


def writebmp(self, filename, width, height, framebuffer):
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header 
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])
        f.close()


def reflect(I, N):
    Lm = mul(I, -1)
    n = mul(N, 2 * dot(Lm, N))
    return norm(sub(Lm, n))

def refract(I, N, refractive_index):  # Implementation of Snell's law
    cosi = -max(-1, min(1, dot(I, N)))
    etai = 1
    etat = refractive_index

    if cosi < 0:  # if the ray is inside the object, swap the indices and invert the normal to get the correct result
      cosi = -cosi
      etai, etat = etat, etai
      N = mul(N, -1)

    eta = etai/etat
    k = 1 - eta**2 * (1 - cosi**2)
    if k < 0:
      return V3(1, 0, 0)

    return norm(sum(
      mul(I, eta),
      mul(N, (eta * cosi - k**(1/2)))
    ))
