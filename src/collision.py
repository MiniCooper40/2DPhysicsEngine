from math import *

from mathlib import *
from src.physicslib import RigidBody
from src.mathlib import Vector


class Collision:

    def __init__(self, start: Vector, normal: Vector, depth: float):
        self.start = start
        self.normal = normal
        self.depth = depth


class CollisionDetector:

    def circle_polygon_collision(self, circle: Circle, polygon: Polygon) -> Collision:
        pass

    def circle_circle_collision(self, circle_a: Circle, circle_b: Circle) -> Collision:
        pass

    def polygon_polygon_collision(self, polygon_a: Polygon, polygon_b: Polygon) -> Collision:
        pass


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
        # print(f'nearest_edge_index = {nearest_edge_index}, min_distance={min_distance}')

        if min_distance >= 0:
            start_vertex_to_circle = circle.position - vertices[nearest_edge_index]
            edge_direction = vertices[(nearest_edge_index + 1) % len(edges)] - vertices[nearest_edge_index]

            if start_vertex_to_circle.dot(edge_direction) <= 0:  # In R1
                # print("in R1")
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
                    # print("in R2")
                    collision_normal = end_vertex_to_circle.normalized().scaled(-1)
                    collision_depth = circle.radius - end_vertex_to_circle.length()
                    collision_start = circle.position + collision_normal.scaled(circle.radius)

                    return Collision(collision_start, collision_normal, collision_depth)
                elif min_distance < circle.radius:
                    # print("in R3")
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
            return Collision(start, normal.scaled(-1), depth)

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


class PhysicalCollisionResolver(CollisionResolver):

    def resolve_collision(self, body_a: RigidBody, body_b: RigidBody, collision: Collision):
        movement_a = body_a.movement_properties
        movement_b = body_b.movement_properties

        mass_a = body_a.physical_properties.mass
        mass_b = body_b.physical_properties.mass

        restitution_a = body_a.physical_properties.restitution
        restitution_b = body_b.physical_properties.restitution

        point_of_collision = collision.start
        normal = collision.normal

        relative_velocity = movement_a.velocity - movement_b.velocity

        impulse = (-(1 + restitution_a) * (relative_velocity.dot(normal))) / (
                normal.dot(normal) * (1 / mass_a + 1 / mass_b))

        # print(f'impulse is {impulse}')

        movement_a.velocity += normal.scaled(impulse / mass_a)
        movement_b.velocity -= normal.scaled(impulse / mass_b)
