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
        axes = []

        vertices = [vertex + polygon.position for vertex in polygon.vertices]

        for index in range(1,len(polygon.vertices)):
            axes.append((polygon.vertices[index]-polygon.vertices[index-1]).normalized_normal())

        axes.append((polygon.vertices[0] - polygon.vertices[-1]).normalized_normal())

        closest_to_circle = vertices[0]
        for vertex in vertices[1:]:
            if (vertex-circle.position).length() < (closest_to_circle-circle.position).length():
                closest_to_circle = vertex

        axes.append((circle.position-closest_to_circle).normalized())

        colliding = True

        for axis in axes:
            circle_center_projection = circle.position.dot(axis)

            circle_start_projection = circle_center_projection-circle.radius
            circle_end_projection = circle_center_projection+circle.radius

            polygon_vertex_projections = [vertex.dot(axis) for vertex in vertices]

            min_polygon_projection = min(polygon_vertex_projections)
            max_polygon_projection = max(polygon_vertex_projections)

            if (circle_start_projection < min_polygon_projection < circle_end_projection) or (circle_start_projection < max_polygon_projection < circle_end_projection) or (min_polygon_projection < circle_start_projection < max_polygon_projection) or (min_polygon_projection < circle_end_projection < max_polygon_projection):
                pass
            else:
                colliding = False
                break

        if colliding:
            print("Colliding, c w/ p")

    def circle_circle_collision(self, circle_a: Circle, circle_b: Circle) -> Collision:
        distance_between = (circle_a.position-circle_b.position).length()
        radius_between = circle_a.radius + circle_b.radius

        colliding = distance_between < radius_between

        if colliding:
            print("Colliding! c w/ c")

    def polygon_polygon_collision(self, polygon_a: Polygon, polygon_b: Polygon) -> Collision:
        a_axes = []
        b_axes = []

        a_vertices = [vertex + polygon_a.position for vertex in polygon_a.vertices]
        b_vertices = [vertex + polygon_b.position for vertex in polygon_b.vertices]

        for index in range(1,len(polygon_a.vertices)):
            a_axes.append((polygon_a.vertices[index]-polygon_a.vertices[index-1]).normalized_normal())

        for index in range(1,len(polygon_b.vertices)):
            b_axes.append((polygon_b.vertices[index]-polygon_b.vertices[index-1]).normalized_normal())

        a_axes.append((polygon_a.vertices[0]-polygon_a.vertices[-1]).normalized_normal())
        b_axes.append((polygon_b.vertices[0] - polygon_b.vertices[-1]).normalized_normal())

        colliding = True

        collision = {
            'distance': 0
        }

        for axis in a_axes:
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

            if (min_b < min_a < max_b) or (min_b < max_a < max_b):
                pass
            elif (min_a < min_b < max_a) or (min_a < max_b < max_a):
                pass
            else:
                colliding = False
                break

        if colliding:
            print('Colliding! p w/ p')


