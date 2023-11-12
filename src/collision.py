from math import *

from mathlib import *
from physicslib import Collision
from src.entity import RigidBody
from src.physicslib import Collision


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

        for index in range(1, len(polygon.vertices)):
            axes.append((polygon.vertices[index] - polygon.vertices[index - 1]).normalized_normal())

        axes.append((polygon.vertices[0] - polygon.vertices[-1]).normalized_normal())

        closest_to_circle = vertices[0]
        for vertex in vertices[1:]:
            if (vertex - circle.position).length() < (closest_to_circle - circle.position).length():
                closest_to_circle = vertex

        axes.append((circle.position - closest_to_circle).normalized())

        colliding = True

        for axis in axes:
            circle_center_projection = circle.position.dot(axis)

            circle_start_projection = circle_center_projection - circle.radius
            circle_end_projection = circle_center_projection + circle.radius

            polygon_vertex_projections = [vertex.dot(axis) for vertex in vertices]

            min_polygon_projection = min(polygon_vertex_projections)
            max_polygon_projection = max(polygon_vertex_projections)

            if (circle_start_projection < min_polygon_projection < circle_end_projection) or (
                    circle_start_projection < max_polygon_projection < circle_end_projection) or (
                    min_polygon_projection < circle_start_projection < max_polygon_projection) or (
                    min_polygon_projection < circle_end_projection < max_polygon_projection):
                pass
            else:
                colliding = False
                break

    def circle_circle_collision(self, circle_a: Circle, circle_b: Circle) -> Collision:
        distance_between = (circle_a.position - circle_b.position).length()
        radius_between = circle_a.radius + circle_b.radius

        colliding = distance_between < radius_between

    def polygon_polygon_collision(self, polygon_a: Polygon, polygon_b: Polygon) -> Collision:
        a_axes = []
        b_axes = []

        a_vertices = [vertex + polygon_a.position for vertex in polygon_a.vertices]
        b_vertices = [vertex + polygon_b.position for vertex in polygon_b.vertices]

        for index in range(1, len(polygon_a.vertices)):
            a_axes.append((polygon_a.vertices[index] - polygon_a.vertices[index - 1]).normalized_normal())

        for index in range(1, len(polygon_b.vertices)):
            b_axes.append((polygon_b.vertices[index] - polygon_b.vertices[index - 1]).normalized_normal())

        a_axes.append((polygon_a.vertices[0] - polygon_a.vertices[-1]).normalized_normal())
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


class SupportPoint:

    def __init__(self, point=Vector(0, 0), distance=-inf, normal=Vector(0, 1)):
        self.point = point
        self.distance = distance
        self.normal = normal

    def __eq__(self, other):
        return self.distance == other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __ge__(self, other):
        return self.distance >= other.distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return f'SupportPoint(point={self.point}, distance={self.distance}, normal={self.normal})'


def find_support_point(polygon, edge_normal, edge_point):
    """
    polygon: the polygon colliding with a particular polygon.  the polygon who supplies vertices for the support point algorithm
    edge_normal:  the normal to the edge being checked for collisions on a particular polygon.  this faces towards the inside of the polygon
    edge_point: a point on the edge whos normal was supplied. given in world coordinates
    """
    support_point = SupportPoint(distance=-inf)
    adjusted_vertices = [vertex + polygon.position for vertex in polygon.vertices]

    for vertex in adjusted_vertices:
        displacement_to_point = vertex - edge_point
        distance_to_point = displacement_to_point.dot(edge_normal)
        temp_support_point = SupportPoint(vertex, distance_to_point, edge_normal)
        if distance_to_point > 0 and temp_support_point > support_point:
            support_point = temp_support_point

    return None if support_point.distance == -inf else support_point


def find_axis_of_least_penetration(polygon_a, polygon_b):
    support_point = SupportPoint(distance=inf)

    normals = []

    for index in range(1, len(polygon_a.vertices)):
        normals.append((polygon_a.vertices[index] - polygon_a.vertices[index - 1]).normalized_normal().scaled(-1))

    normals.append((polygon_a.vertices[0] - polygon_a.vertices[-1]).normalized_normal().scaled(-1))

    adjusted_vertices = [vertex + polygon_a.position for vertex in polygon_a.vertices]

    for (vertex, normal) in zip(adjusted_vertices, normals):
        temp_support_point = find_support_point(polygon_b, normal, vertex)

        if temp_support_point is None:
            return None
        if temp_support_point < support_point:
            support_point = temp_support_point

    return support_point if support_point.distance != inf else None


class EfficientSATCollisionDetector(CollisionDetector):

    def circle_polygon_collision(self, circle: Circle, polygon: Polygon) -> Collision | None:

        min_distance = -inf
        nearest_edge_index = None

        vertices = polygon.absolute_vertices()
        edge_normals = polygon.edge_normals()
        edges = polygon.edges()

        for edge_index in range(0, len(edges)):
            displacement_to_center = circle.position - vertices[edge_index]
            distance_to_center = displacement_to_center.dot(edge_normals[edge_index])

            if distance_to_center > min_distance:
                min_distance = distance_to_center
                nearest_edge_index = edge_index
        print(f'nearest_edge_index = {nearest_edge_index}, min_distance={min_distance}')

        if min_distance >= 0:
            start_vertex_to_circle = circle.position - vertices[nearest_edge_index]
            edge_direction = vertices[(nearest_edge_index + 1) % len(edges)] - vertices[nearest_edge_index]

            if start_vertex_to_circle.dot(edge_direction) <= 0:  # In R1
                print("in R1")
                if start_vertex_to_circle.length() > circle.radius:
                    return None

                collision_normal = start_vertex_to_circle.normalized().scaled(-1)
                collision_depth = circle.radius - start_vertex_to_circle.length()
                collision_start = circle.position + collision_normal.scaled(circle.radius)

                return Collision(collision_start, collision_normal, collision_depth)

            else:
                end_vertex_to_circle = circle.position - vertices[(nearest_edge_index + 1) % len(edges)]
                edge_direction = edge_direction.scaled(-1)

                if end_vertex_to_circle.dot(edge_direction) <= 0:  # In R2
                    if end_vertex_to_circle.length() > circle.radius:
                        return None
                    print("in R2")
                    collision_normal = end_vertex_to_circle.normalized().scaled(-1)
                    collision_depth = circle.radius - end_vertex_to_circle.length()
                    collision_start = circle.position + collision_normal.scaled(circle.radius)

                    return Collision(collision_start, collision_normal, collision_depth)
                elif min_distance < circle.radius:
                    print("in R3")
                    to_circle_center = edge_normals[nearest_edge_index].scaled(circle.radius)

                    collision_depth = circle.radius - min_distance
                    collision_normal = edge_normals[nearest_edge_index].scaled(-1)
                    collision_start = circle.position - to_circle_center

                    return Collision(collision_start, collision_normal, collision_depth)
        else:
            to_circle_center = edge_normals[nearest_edge_index].scaled(-min_distance)
            to_circle_radius = edge_normals[nearest_edge_index].scaled(circle.radius)

            depth = circle.radius - min_distance
            normal = edge_normals[nearest_edge_index]
            start = circle.position + to_circle_center

            return Collision(start, normal, depth)

    def circle_circle_collision(self, circle_a: Circle, circle_b: Circle) -> Collision | None:
        distance_between = (circle_a.position - circle_b.position).length()
        radius_between = circle_a.radius + circle_b.radius

        colliding = distance_between < radius_between

        if colliding:
            normal = (circle_b.position - circle_a.position).normalized()
            depth = radius_between - distance_between
            start = circle_a.position + normal.scaled(circle_a.radius)
            return Collision(start, normal, depth)

        return None

    def polygon_polygon_collision(self, polygon_a: Polygon, polygon_b: Polygon) -> Collision | None:
        support_a = find_axis_of_least_penetration(polygon_a, polygon_b)
        support_b = find_axis_of_least_penetration(polygon_b, polygon_a)

        if support_a is not None and support_b is not None:

            if support_a < support_b:
                start = support_a.point
                return Collision(support_a.point, support_a.normal, support_a.distance)

            if support_a >= support_b:
                start = support_b.point
                return Collision(support_b.point, support_b.normal, support_b.distance)

        return None


class CollisionResolver:

    def resolve_collision(self, body_a: RigidBody, body_b: RigidBody, collision):
        pass


class SimpleCollisionResolver(CollisionResolver):

    def resolve_collision(self, body_a: RigidBody, body_b: RigidBody, collision):
        normal = collision.normal
        depth = collision.depth
        start = collision.start

        correction = normal.scaled(depth)

        body_a.move(correction.scaled(0.5))
        body_b.move(correction.scaled(-0.5))
