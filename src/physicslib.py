
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
    """
    A shape that represents a region of space with physical significance.
    """

    def accept_hitbox_renderer(self, hitbox_renderer, **kwargs):
        """"Visitor pattern for rendering hitbox"""
        pass

    def move(self, displacement):
        pass

    def rotate(self, degrees):
        pass


class CircleHitbox(Hitbox):

    def __init__(self, circle: Circle,):
        self.circle = circle

    def move(self, displacement: Vector):
        self.circle.translate(displacement)

    def rotate(self, degrees):
        self.circle.transform(Matrix.rotate(degrees))

    def accept_hitbox_renderer(self, hitbox_renderer,  **kwargs):
        hitbox_renderer.render_circle_hitbox(self,  **kwargs)


class PolygonHitbox(Hitbox):

    def __init__(self, polygon):
        self.polygon = polygon

    def move(self, displacement: Vector):
        self.polygon.translate(displacement)

    def rotate(self, degrees):
        self.polygon.rotate(degrees)

    def accept_hitbox_renderer(self, hitbox_renderer, **kwargs):
        hitbox_renderer.render_polygon_hitbox(self, **kwargs)


class Body:
    """
    A particular region of space with some physical significance.  This region may move, and contact with it by
    another body may have significance for both bodies involved.
    """

    def get_hitbox(self):
        pass

    def get_movement_properties(self, movement_properties):
        pass

    def set_movement_properties(self, movement_properties):
        pass

    def move(self, displacement):
        pass

    def rotate(self, angle):
        pass


class RigidBody(Body):
    """
    A body that represents a solid, physical object that does not deform upon collision (a rigid body).
    """

    def __init__(self, hitbox: Hitbox, physical_properties: PhysicalProperties = PhysicalProperties()):
        self.hitbox = hitbox
        self.physical_properties = physical_properties

    def get_hitbox(self):
        return self.hitbox

    def get_physical_properties(self):
        return self.physical_properties

    def move(self, displacement):
        self.hitbox.move(displacement)

    def rotate(self, degrees):
        self.hitbox.rotate(degrees)


class Region:
    """
    A region of coordinates in space.  A region might have impact on the physical properties, movement, logic,
    etc... of bodies in a particular region.
    """

    def get_hitbox(self):
        pass
