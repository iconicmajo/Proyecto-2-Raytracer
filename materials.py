#MATERIALS

from mathfunc import color
from dataclasses import dataclass

class Material(object):
  def __init__(self,diffuse,  albedo=(1, 0, 0, 0), spec=0, refractive_index=1):
    self.diffuse = diffuse
    self.albedo = albedo
    self.spec = spec
    self.refractive_index = refractive_index

ivory = Material(diffuse=color(100, 100, 80), albedo=(0.6, 0.3, 0.1, 0), spec=50)
rubber = Material(diffuse=color(80, 0, 0), albedo=(0.9, 0.1, 0, 0, 0), spec=10)
mirror = Material(diffuse=color(255, 255, 255), albedo=(0, 10, 0.8, 0), spec=1425)
glass = Material(diffuse=color(150, 180, 200), albedo=(0, 0.5, 0.1, 0.8), spec=125, refractive_index=1.5)
brown = Material(diffuse = color(212, 163, 108),albedo = (0.6, 0.3, 0.1, 0), spec = 5)
darkbrown = Material(diffuse = color(143, 86, 23),albedo = (0.6, 0.3, 0.1, 0), spec = 5)
green = Material(diffuse = color(139, 150, 18),albedo=(0.9, 0.1, 0, 0, 0), spec=10)
snow = Material(diffuse = color(209, 232, 237),albedo = (0.6, 0.3, 0.1, 0), spec = 5)
coal = Material(diffuse = color(0,0,0),albedo = (0.6, 0.3, 0.1, 0), spec = 5)
carrot = Material(diffuse = color(227, 110, 14), albedo=(0.9, 0.1, 0, 0, 0), spec=10)
white = Material(diffuse = color(255, 255, 255),albedo = (0.6, 0.3, 0.1, 0), spec = 5)
silver = Material(diffuse = color(145, 145, 145),albedo = (0.6, 0.3, 0.1,0), spec = 5)
red = Material(diffuse=color(80, 0, 0), albedo=(0.9, 0.1, 0, 0, 0), spec=10)
yellow = Material(diffuse = color(100, 100, 80), albedo=(0.6, 0.3, 0.1, 0), spec=5)
