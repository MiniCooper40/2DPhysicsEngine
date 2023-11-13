from physicslib import *
from src.physicslib import RigidBody


class Sprite:

    def __init__(self, image=None, angle=0, position=Vector(0, 0)):
        self.image = image
        self.angle = angle
        self.position = position


class RenderProperties:

    def __init__(self, sprite=Sprite(), movement_properties=MovementProperties()):
        self.sprite = sprite
        self.movement_properties = movement_properties


class PhysicalEntity:

    def __init__(self, rigid_body: RigidBody, render_properties: RenderProperties = None):
        self.rigid_body = rigid_body
        self.render_properties = render_properties
