from physicslib import *


class Sprite:

    def __init__(self, image=None, angle=0, position=Vector(0, 0)):
        self.image = image
        self.angle = angle
        self.position = position


class RenderProperties:

    def __init__(self, sprite=Sprite(), movement_properties=MovementProperties()):
        self.sprite = sprite
        self.movement_properties = movement_properties


class Body:

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

    def intersects_with(self, other):
        pass


class RigidBody(Body):

    def __init__(self, hitbox: Hitbox, physical_properties: PhysicalProperties = PhysicalProperties()):
        self.hitbox = hitbox
        self.physical_properties = physical_properties

    def get_hitbox(self):
        return self.hitbox

    def get_physical_properties(self):
        return self.physical_properties

    def collision_with(self, other: Body):
        return self.get_hitbox().accept_collision(other.get_hitbox())

    def intersects_with(self, other: Body):
        return self.get_hitbox().accept_intersection(other.get_hitbox())

    def move(self, displacement):
        self.hitbox.move(displacement)

    def rotate(self, degrees):
        self.hitbox.rotate(degrees)


class PhysicalEntity:

    def __init__(self, rigid_body: RigidBody, render_properties: RenderProperties = None):
        self.rigid_body = rigid_body
        self.render_properties = render_properties
