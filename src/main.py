
from display import *


def on_key_pressed(key):
    print(f'key pressed: {key}')


h = CircleHitbox(Circle(radius=40, position=Vector(60, 60)))
r = RigidBody(hitbox=h)
p: PhysicalEntity = PhysicalEntity(r)

h2 = PolygonHitbox(
    Polygon([Vector(-20, 20), Vector(20, 20), Vector(20, -20), Vector(-20, -20)], position=Vector(60, 60)))
r2 = RigidBody(hitbox=h2)
p2: PhysicalEntity = PhysicalEntity(r2)

h3 = PolygonHitbox(
    Polygon([Vector(-25, 25), Vector(20, 20), Vector(20, -20), Vector(-30, -35)], position=Vector(160, 60)))
r3 = RigidBody(hitbox=h3)
p3: PhysicalEntity = PhysicalEntity(r3)

h4 = CircleHitbox(Circle(radius=30, position=Vector(200, 200)))
r4 = RigidBody(hitbox=h4)
p4: PhysicalEntity = PhysicalEntity(r4)

ps = [p, p2, p3, p4]
e = GameEnvironment(ps)

canvas = PhysicsCanvas(e)
