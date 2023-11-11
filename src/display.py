import itertools
import time

from mathlib import *
from tkinter import *
from entity import *
from physicslib import *
import math
from game_environment import *
from src.collision import SATCollisionDetector

speed = 8
angular_velocity = 0.3


class PhysicsCanvas:

    def rotate_right(self, key):
        self.environment.selected_entity.rigid_body.rotate(degrees=angular_velocity)
        self.draw()

    def rotate_left(self, key):
        self.environment.selected_entity.rigid_body.rotate(degrees=-angular_velocity)
        self.draw()

    def move_up(self, key):
        self.environment.selected_entity.rigid_body.move(Vector(0, -speed))
        self.draw()

    def move_down(self, key):
        self.environment.selected_entity.rigid_body.move(Vector(0, speed))
        self.draw()

    def move_right(self, key):
        self.environment.selected_entity.rigid_body.move(Vector(speed, 0))
        self.draw()

    def move_left(self, key):
        self.environment.selected_entity.rigid_body.move(Vector(-speed, 0))
        self.draw()

    def next_selection(self, key):
        self.environment.select_next_entity()
        self.draw()

    def game_loop(self):
        FPS = 60
        SPF = 60 / FPS
        last_time = time.time()
        delta_time = 0
        print(last_time)
        while True:
            current_time = time.time()
            delta_time = delta_time + (current_time - last_time)
            last_time = current_time
            if SPF <= delta_time:
                delta_time = 0
                print(f"delta: {delta_time}")
            self.root.update()

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

        self.collision_detector = SATCollisionDetector()

        self.canvas.pack()
        self.game_loop()
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        if self.is_debugging:
            for entity in self.environment.physical_entities:
                selected = entity is self.environment.selected_entity
                print(f"entity is selected? {selected}")
                self.hitbox_renderer.render(entity.rigid_body.get_hitbox(), selected=selected)

        for (a,b) in itertools.product(self.environment.physical_entities, repeat=2):
            if a is b:
                continue
            r_a = a.rigid_body
            r_b = b.rigid_body

            h_a = r_a.get_hitbox()
            h_b = r_b.get_hitbox()

            if isinstance(h_a,PolygonHitbox) and isinstance(h_b, PolygonHitbox):
                self.collision_detector.polygon_polygon_collision(h_a.polygon, h_b.polygon)

            elif isinstance(h_a,PolygonHitbox) and isinstance(h_b, CircleHitbox):
                self.collision_detector.circle_polygon_collision(h_b.circle, h_a.polygon)

            elif isinstance(h_a,CircleHitbox) and isinstance(h_b, PolygonHitbox):
                self.collision_detector.circle_polygon_collision(h_a.circle, h_b.polygon)

            elif isinstance(h_a, CircleHitbox) and isinstance(h_b, CircleHitbox):
                self.collision_detector.circle_circle_collision(h_a.circle, h_b.circle)

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

    def render(self, hitbox: Hitbox, **kwargs):
        hitbox.accept_hitbox_renderer(self, **kwargs)

    def render_polygon_hitbox(self, polygon_hitbox: PolygonHitbox, **kwargs):
        polygon = polygon_hitbox.polygon
        coordinates = []
        for vertex in polygon.vertices:
            coordinates.append(vertex.x + polygon.position.x)
            coordinates.append(vertex.y + polygon.position.y)

        color = 'red' if kwargs.get('selected', False) else 'black'

        self.canvas.create_polygon(coordinates, fill="", outline=color)

    def render_circle_hitbox(self, circle_hitbox: CircleHitbox,  **kwargs):
        circle = circle_hitbox.circle
        x_start = circle.position.x - circle.radius
        y_start = circle.position.y - circle.radius
        x_end = circle.position.x + circle.radius
        y_end = circle.position.y + circle.radius

        print(circle)

        color = 'red' if kwargs.get('selected', False) else 'black'

        self.canvas.create_oval(x_start, y_start, x_end, y_end, outline=color)
