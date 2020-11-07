from mathfunc import writebmp, color, norm, V3, sub, dot, reflect, length, mul, sum, refract
from sphere import Sphere
from math import pi, tan
from cube import Cube
from envmap import Envmap
from pyramid import Pyramid
from materials import coal, yellow, silver, mirror, green, darkbrown, brown, red
import random
from light import *


BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

BACKGROUND = color(0, 0, 0)

MAX_RECURSION_DEPTH = 3


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.activeTexture = WHITE
        self.envMap = None
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.activeTexture for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename='out.bmp'):
        writebmp(filename, self.width, self.height, self.framebuffer)

    def point(self, x, y, selectColor=None):
        try:
            self.framebuffer[y][x] = selectColor or self.activeTexture
        except:
            pass

    def sceneIntersect(self, origin, direction):
        zbuffer = float('inf')
        
        material = None
        intersect = None
        
        for obj in self.scene:
            hit = obj.rayIntersect(origin, direction)
            if hit is not None:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit
        return material, intersect

    def castRay(self, origin, direction, recursion = 0):
        material, intersect = self.sceneIntersect(origin, direction)
        
        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envMap:
                return self.envMap.getColor(direction)
            return self.activeTexture
        
        lightDir = norm(sub(self.light.position, intersect.point))
        lightDistance = length(sub(self.light.position, intersect.point))
        
        offsetNormal = mul(intersect.normal, 1.1)
        shadowOrigin = sub(intersect.point, offsetNormal) if dot(lightDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
        shadowMaterial, shadowIntersect = self.sceneIntersect(shadowOrigin, lightDir)
        shadowIntensity = 0

        if shadowMaterial and length(sub(shadowIntersect.point, shadowOrigin)) < lightDistance:
            shadowIntensity = 0.9

        intensity = self.light.intensity * max(0, dot(lightDir, intersect.normal)) * (1 - shadowIntensity)

        reflection = reflect(lightDir, intersect.normal)
        specularIntensity = self.light.intensity * (
            max(0, -dot(reflection, direction)) ** material.spec
        )

        if material.albedo[2] > 0:
            reflectDir = reflect(direction, intersect.normal)
            reflectOrigin = sub(intersect.point, offsetNormal) if dot(reflectDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
            reflectedColor = self.castRay(reflectOrigin, reflectDir, recursion + 1)
        else:
            reflectedColor = self.activeTexture

        if material.albedo[3] > 0:
            refractDir = refract(direction, intersect.normal, material.refractionIndex)
            refractOrigin = sub(intersect.point, offsetNormal) if dot(refractDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
            refractedColor = self.castRay(refractOrigin, refractDir, recursion + 1)
        else:
            refractedColor = self.activeTexture

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specularIntensity * material.albedo[1]
        reflected = reflectedColor * material.albedo[2]
        refracted = refractedColor * material.albedo[3]
        
        return diffuse + specular + reflected + refracted


    def render(self):
        fov = int(pi / 2) # field of view
        for y in range(self.height):
            for x in range(self.width):
                #if random.randint(0,1) !=0:
                #    continue
                i = (2 * (x + 0.5) / self.width - 1) * self.width / self.height * tan(fov / 2)
                j = (2 * (y + 0.5) / self.height - 1) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                self.framebuffer[y][x] = self.castRay(V3(0, 0, 0), direction)

    def gradientBackground(self):
        for x in range(self.width):
            for y in range(self.height):
                r = int((x / self.width) * 255) if x / self.width < 1 else 1
                g = int((y / self.height) * 255) if y / self.height < 1 else 1
                b = 0
                self.framebuffer[y][x] = color(r, g, b)
    


r = Raytracer(800, 500)
#r.envMap = Envmap('sunset.bmp')
r.light = Light(
    position = V3(0, 0, 20),
    intensity = 1.5
)
r.scene = [
    
    #grama
    Cube(V3(0, -4, -2), 6,  mirror),
    #reflejo
    #Cube(V3(0, -3.5, -2), 4, mirror),

    #Sol
    Sphere(V3(7.5, 4, -12), 2, red),

    #arbol
    Pyramid([V3(-5, 0, -10), V3(-6.5, 5, -10), V3(-8, 0, -10), V3(-5, 0, -10)], green),
    Cube(V3(-8, -0.2, -12), 0.8, darkbrown),
    Cube(V3(-8, -1, -12), 0.8, darkbrown),
    
    #inicio de piramide 
    Cube(V3(0, -2.5, -12), 1.5, brown),
    Cube(V3(1.5, -2, -12), 1.5, brown),
    Cube(V3(3, -1.5, -12), 1.5, brown),
    Cube(V3(-1.5, -2, -12), 1.5, brown),
    Cube(V3(-3, -1.5, -12), 1.5, brown),

    #Segundo nivel 
    Cube(V3(0, -1, -12), 1.25, brown),
    Cube(V3(1.3, -0.75, -12), 1.25, brown),
    Cube(V3(2.5, -0.50, -12), 1.25, brown),
    Cube(V3(-1.3, -0.75, -12), 1.25, brown),
    Cube(V3(-2.5, -0.50, -12), 1.25, brown),

    #tercer nivel
    Cube(V3(0, 0, -12), 1.25, brown),
    Cube(V3(1.3, 0.25, -12), 1.25, brown),
    Cube(V3(2.5, 0.50, -12), 1.25, brown),
    Cube(V3(-1.3, 0.25, -12), 1.25, brown),
    Cube(V3(-2.5, 0.50, -12), 1.25, brown),

    #piramides 
    Pyramid([V3(0.3, 0.6, -10), V3(0, 3.6, -10), V3(-0.6, 0.6, -10), V3(0.6, 0.6, -10)], brown),
    Pyramid([V3(-0.6, 0.8, -10), V3(-1.1, 4, -10), V3(-1.6, 0.8, -10), V3(-0.3, 0.8, -10)], brown),
    Pyramid([V3(0.6, 0.8, -10), V3(1.1, 4, -10), V3(1.6, 0.8, -10), V3(0.3, 0.8, -10)], brown),
    Pyramid([V3(2.6, 0.8, -10), V3(2.2, 4, -10), V3(1.3, 0.8, -10), V3(2.6, 0.8, -10)], brown),
    Pyramid([V3(-2.6, 0.8, -10), V3(-2.2, 4, -10), V3(-1.3, 0.8, -10), V3(-2.6, 0.8, -10)], brown),
    

]
r.render()

r.write()

'''
#Sol
    Sphere(V3(7.5, 4, -12), 2, red),

    #arbol
    Pyramid([V3(-5, 0, -10), V3(-6.5, 5, -10), V3(-8, 0, -10), V3(-5, 0, -10)], green),
    Cube(V3(-8, -0.2, -12), 0.8, darkbrown),
    Cube(V3(-8, -1, -12), 0.8, darkbrown),

    #grama
    Cube(V3(0, -4, -2), 6, green),
    reflejo
    Cube(V3(0, -3.99, -2), 4, mirror),
    
    #inicio de piramide 
    Cube(V3(0, -2.5, -12), 1.5, brown),
    Cube(V3(1.5, -2, -12), 1.5, brown),
    Cube(V3(3, -1.5, -12), 1.5, brown),
    Cube(V3(-1.5, -2, -12), 1.5, brown),
    Cube(V3(-3, -1.5, -12), 1.5, brown),

    #Segundo nivel 
    Cube(V3(0, -1, -12), 1.25, brown),
    Cube(V3(1.3, -0.75, -12), 1.25, brown),
    Cube(V3(2.5, -0.50, -12), 1.25, brown),
    Cube(V3(-1.3, -0.75, -12), 1.25, brown),
    Cube(V3(-2.5, -0.50, -12), 1.25, brown),

    #tercer nivel
    Cube(V3(0, 0, -12), 1.25, brown),
    Cube(V3(1.3, 0.25, -12), 1.25, brown),
    Cube(V3(2.5, 0.50, -12), 1.25, brown),
    Cube(V3(-1.3, 0.25, -12), 1.25, brown),
    Cube(V3(-2.5, 0.50, -12), 1.25, brown),

    #piramides 
    Pyramid([V3(0.3, 0.6, -10), V3(0, 3.6, -10), V3(-0.6, 0.6, -10), V3(0.6, 0.6, -10)], brown),
    Pyramid([V3(-0.6, 0.8, -10), V3(-1.1, 4, -10), V3(-1.6, 0.8, -10), V3(-0.3, 0.8, -10)], brown),
    Pyramid([V3(0.6, 0.8, -10), V3(1.1, 4, -10), V3(1.6, 0.8, -10), V3(0.3, 0.8, -10)], brown),
    Pyramid([V3(2.6, 0.8, -10), V3(2.2, 4, -10), V3(1.3, 0.8, -10), V3(2.6, 0.8, -10)], brown),
    Pyramid([V3(-2.6, 0.8, -10), V3(-2.2, 4, -10), V3(-1.3, 0.8, -10), V3(-2.6, 0.8, -10)], brown),
'''
