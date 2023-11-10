from mathlib import *
from tkinter import *
from entity import *
from physicslib import *
import math
from game_environment import *

speed = 8
angular_velocity = 0.3


class GameCanvas:

    def rotate_right(self, key):
        self.environment.selected_entity.rotate(degrees=angular_velocity)
        self.draw()

    def rotate_left(self, key):
        self.environment.selected_entity.rotate(degrees=-angular_velocity)
        self.draw()

    def move_up(self, key):
        self.environment.selected_entity.move(Vector(0, -speed))
        self.draw()

    def move_down(self, key):
        self.environment.selected_entity.move(Vector(0, speed))
        self.draw()

    def move_right(self, key):
        self.environment.selected_entity.move(Vector(speed, 0))
        self.draw()

    def move_left(self, key):
        self.environment.selected_entity.move(Vector(-speed, 0))
        self.draw()

    def next_selection(self, key):
        self.environment.selected_entity = self.environment.physical_entities[-1]

    def __init__(self, environment: GameEnvironment, is_debugging=True):
        self.is_debugging = is_debugging
        self.environment = environment
        self.root = Tk()
        self.canvas = Canvas(width=500, height=400)
        self.hitbox_renderer = TkinterHitboxRenderer(self.canvas)

        self.root.bind('w', self.move_up)
        self.root.bind('a', self.move_left)
        self.root.bind('s', self.move_down)
        self.root.bind('d', self.move_right)
        self.root.bind('t', self.next_selection)
        self.root.bind('e', self.rotate_right)
        self.root.bind('q', self.rotate_left)

        self.canvas.pack()
        self.canvas.mainloop()
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if self.is_debugging:
            for entity in self.environment.physical_entities:
                self.hitbox_renderer.render(entity.rigid_body.get_hitbox())

        self.root.update()


class HitboxRenderer:

    def render(self, hitbox: Hitbox):
        pass

    def render_polygon_hitbox(self, polygon_hitbox: PolygonHitbox):
        pass

    def render_circle_hitbox(self, circle_hitbox: CircleHitbox):
        pass


class TkinterHitboxRenderer(HitboxRenderer):

    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def render(self, hitbox: Hitbox):
        hitbox.accept_hitbox_renderer(self)

    def render_polygon_hitbox(self, polygon_hitbox: PolygonHitbox):
        polygon = polygon_hitbox.polygon
        coordinates = []
        for vertex in polygon.vertices:
            coordinates.append(vertex.x + polygon.position.x)
            coordinates.append(vertex.y + polygon.position.y)

        self.canvas.create_polygon(coordinates, fill="", outline="black")

    def render_circle_hitbox(self, circle_hitbox: CircleHitbox):

        circle = circle_hitbox.circle
        x_start = circle.position.x - circle.radius
        y_start = circle.position.y - circle.radius
        x_end = circle.position.x + circle.radius
        y_end = circle.position.y + circle.radius

        print(circle)

        self.canvas.create_oval(x_start, y_start, x_end, y_end)
