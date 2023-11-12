
from mathlib import *


class MovementProperties:
    """Properties related to the physical movement of an object"""

    def __init__(self, velocity=Vector(0, 0), acceleration=Vector(0, 0), angular_velocity=0):
        self.velocity = velocity
        self.acceleration = acceleration
        self.angular_velocity = angular_velocity
        self.angular_acceleration = 0


class PhysicalProperties:
    """Properties related to the physical composition of an object"""

    def __init__(self, mass=1, restitution=0.5):
        self.mass = mass
        self.restitution = restitution


class Hitbox:

    def accept_intersection(self, other_hitbox):
        """Visitor pattern for intersection checking"""
        pass

    def accept_collision(self, other_hitbox):
        """Visitor pattern for collision calculating"""
        pass

    def accept_hitbox_renderer(self, hitbox_renderer, **kwargs):
        """"Visitor pattern for rendering hitbox"""
        pass

    def move(self, displacement):
        pass

    def rotate(self, degrees):
        pass


class CircleHitbox(Hitbox):

    def __init__(self, circle: Circle, intersects_circle=None, intersects_polygon=None, polygon_collision=None, circle_collision=None):
        self.circle = circle
        self.intersects_circle = intersects_circle
        self.intersects_polygon = intersects_polygon
        self.polygon_collision = polygon_collision
        self.circle_collision = circle_collision

    def accept_intersection(self, other_hitbox):
        return other_hitbox.intersects_circle_hitbox(self)

    def accept_collision(self, other_hitbox):
        return other_hitbox.collision_with_circle_hitbox(self)

    def move(self, displacement: Vector):
        self.circle.translate(displacement)

    def rotate(self, degrees):
        self.circle.transform(Matrix.rotate(degrees))

    def accept_hitbox_renderer(self, hitbox_renderer,  **kwargs):
        hitbox_renderer.render_circle_hitbox(self,  **kwargs)


class PolygonHitbox(Hitbox):

    def __init__(self, polygon, intersects_circle=None, intersects_polygon=None, polygon_collision=None, circle_collision=None):
        self.polygon = polygon
        self.intersects_circle = intersects_circle
        self.intersects_polygon = intersects_polygon
        self.polygon_collision = polygon_collision
        self.circle_collision = circle_collision

    def accept_intersection(self, other_hitbox):
        return other_hitbox.intersects_polygon_hitbox(self)

    def accept_collision(self, other_hitbox):
        return other_hitbox.collision_with_polygon_hitbox(self)

    def move(self, displacement: Vector):
        self.polygon.translate(displacement)

    def rotate(self, degrees):
        self.polygon.rotate(degrees)

    def accept_hitbox_renderer(self, hitbox_renderer, **kwargs):
        hitbox_renderer.render_polygon_hitbox(self, **kwargs)


class Collision:

    def __init__(self, start: Vector, normal: Vector, depth: float):
        self.start = start
        self.normal = normal
        self.depth = depth


