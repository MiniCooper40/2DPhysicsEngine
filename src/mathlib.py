import math
from copy import deepcopy


class Vector:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        length = self.length()
        return Vector(self.x / length, self.y / length)

    def normalized_normal(self):
        length = self.length()
        return Vector(-self.y/length, self.x/length)

    def normal(self):
        return Vector(-self.y, self.x)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def scaled(self, scaler):
        return Vector(self.x * scaler, self.y * scaler)

    def __repr__(self):
        return f'[x={self.x},y={self.y}]'


class Matrix:

    def __init__(self, vectors=[]):
        self.vectors = vectors

    def __mul__(self, multiplier):
        if isinstance(multiplier, Vector):
            x = self.vectors[0].x * multiplier.x + self.vectors[1].x * multiplier.y
            y = self.vectors[0].y * multiplier.x + self.vectors[1].y * multiplier.y
            return Vector(x, y)

    def __repr__(self):
        return f'{self.vectors}'

    @staticmethod
    def rotate(degrees):
        v1 = Vector(math.cos(degrees), math.sin(degrees))
        v2 = Vector(-math.sin(degrees), math.cos(degrees))
        return Matrix([v1, v2])


class Shape:

    def __init__(self, position=Vector(0, 0), direction=Vector(0, 1)):
        self.position = position
        self.direction = direction


class Circle(Shape):

    def __init__(self, position=Vector(0, 0), radius=1):
        Shape.__init__(self, position)
        self.radius = float(radius)

    def __repr__(self):
        return f'Circle(radius={self.radius}, position={self.position})'

    def display(self, canvas):
        x_start = self.position.x - self.radius
        y_start = self.position.y - self.radius
        x_end = self.position.x + self.radius
        y_end = self.position.y + self.radius

        canvas.create_oval(x_start, y_start, x_end, y_end)

    def transform(self, matrix):
        print(matrix)

    def translate(self, displacement):
        self.position = self.position + displacement


class Polygon(Shape):

    def __init__(self, vertices=None, position=Vector(0, 0), angle = 0):
        Shape.__init__(self, position)
        if vertices is None:
            vertices = []
        self.vertices = vertices
        self.initial_vertices = deepcopy(self.vertices)
        self.angle = 0

    def __repr__(self):
        return f'Polygon(vertices={self.vertices}, position={self.position})'

    def rotate(self, degrees):
        self.angle += degrees
        transformation = Matrix.rotate(self.angle)
        self.vertices = [transformation * vertex for vertex in self.initial_vertices]

    def translate(self, displacement):
        self.position = self.position + displacement

    def edges(self):
        edges = []

        for index in range(1, len(self.vertices)):
            edges.append((self.vertices[index] - self.vertices[index - 1]))

        edges.append((self.vertices[0] - self.vertices[-1]))
        return edges

    def edge_normals(self):
        return [edge.normal().normalized() for edge in self.edges()]

    def absolute_vertices(self):
        return [vertex + self.position for vertex in self.vertices]
