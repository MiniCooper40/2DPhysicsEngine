from math import *

from mathlib import *
from physicslib import Collision


class CollisionDetector:

    def circle_polygon_collision(self, circle: Circle, polygon: Polygon) -> Collision:
        pass

    def circle_circle_collision(self, circle_a: Circle, circle_b: Circle) -> Collision:
        pass

    def polygon_polygon_collision(self, polygon_a: Polygon, polygon_b: Polygon) -> Collision:
        pass


class SATCollisionDetector(CollisionDetector):

    def circle_polygon_collision(self, circle: Circle, polygon: Polygon) -> Collision:
        pass

    def circle_circle_collision(self, circle_a: Circle, circle_b: Circle) -> Collision:
        pass

    def polygon_polygon_collision(self, polygon_a: Polygon, polygon_b: Polygon) -> Collision:
        axes = []

        a_vertices = [vertex + polygon_a.position for vertex in polygon_a.vertices]
        b_vertices = [vertex + polygon_b.position for vertex in polygon_b.vertices]

        for index in range(1,len(polygon_a.vertices)):
            axes.append((polygon_a.vertices[index]-polygon_a.vertices[index-1]).normalized_normal())

        for index in range(1,len(polygon_b.vertices)):
            axes.append((polygon_b.vertices[index]-polygon_b.vertices[index-1]).normalized_normal())

        axes.append((polygon_a.vertices[0]-polygon_a.vertices[-1]).normalized_normal())
        axes.append((polygon_b.vertices[0] - polygon_b.vertices[-1]).normalized_normal())

        colliding = True

        for axis in axes:
            min_a = a_vertices[0].dot(axis)
            min_b = b_vertices[0].dot(axis)

            max_a = min_a
            max_b = min_b

            for vertex in a_vertices[1:]:
                distance = vertex.dot(axis)
                if distance > max_a:
                    max_a = distance
                elif distance <= min_a:
                    min_a = distance

            for vertex in b_vertices[1:]:
                distance = vertex.dot(axis)
                if distance > max_b:
                    max_b = distance
                elif distance <= min_b:
                    min_b = distance

            if (min_b < min_a < max_b) or (min_b < max_a < max_b) or (min_a < min_b < max_a) or (min_a < max_b < max_a):
                pass
            else:
                colliding = False
                break

        if colliding:
            print(f'colliding? {colliding}')


