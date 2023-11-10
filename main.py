
from display import *


def on_key_pressed(key):
    print(f'key pressed: {key}')


# h = CircleHitbox(Circle(radius=40, position=Vector(60, 60)))
# r = RigidBody(hitbox=h)
# p: PhysicalEntity = PhysicalEntity(r)

h2 = PolygonHitbox(
    Polygon([Vector(-20, 20), Vector(20, 20), Vector(20, -20), Vector(-20, -20)], position=Vector(60, 60)))
r2 = RigidBody(hitbox=h2)
p2: PhysicalEntity = PhysicalEntity(r2)

ps = [p2]
e = GameEnvironment(ps)

canvas = GameCanvas(e)
