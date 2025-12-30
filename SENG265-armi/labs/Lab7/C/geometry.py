# Replace this file with your solution from part B.
import math

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(%r, %r)" % (self.x, self.y)

    def delta_x(self, dx):
        return Point(self.x + dx, self.y)
    def delta_y(self, dy):
        return Point(self.x, self.y + dy)
    def translate(self, dx, dy):
        return Point(self.x + dx, self.y + dy)
class Circle:
    def __init__(self, center, radius):
       self.center = center
       self.radius = radius
    def __repr__(self):
       return f"Circle({self.center}, {self.radius})"
    def area(self):
        return math.pi * self.radius ** 2
    def perimeter(self):
        return 2* math.pi * self.radius
    def translate(self, dx, dy):
        new_center = self.center.translate(dx, dy)
        return Circle(new_center, self.radius)
