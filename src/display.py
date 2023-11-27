import itertools
import time

from tkinter import *
from environment import *
from src.collision import EfficientSATCollisionDetector, \
    SimpleCollisionResolver, Collision, PhysicalCollisionResolver

speed = 4
angular_velocity = 0.3


class PhysicsCanvas:

    def rotate_right(self, key):
        # self.environment.selected_entity.rigid_body.rotate(degrees=angular_velocity)
        self.environment.selected_entity.rigid_body.get_movement_properties().angular_velocity += 0.3
        self.draw()

    def rotate_left(self, key):
        # self.environment.selected_entity.rigid_body.rotate(degrees=-angular_velocity)
        self.environment.selected_entity.rigid_body.get_movement_properties().angular_velocity -= 0.3
        self.draw()

    def move_up(self, key):
        # self.environment.selected_entity.rigid_body.move(Vector(0, -speed))
        self.environment.selected_entity.rigid_body.movement_properties.velocity += Vector(0, -speed)
        self.draw()

    def move_down(self, key):
        # self.environment.selected_entity.rigid_body.move(Vector(0, speed))
        self.environment.selected_entity.rigid_body.movement_properties.velocity += Vector(0, speed)
        self.draw()

    def move_right(self, key):
        # self.environment.selected_entity.rigid_body.move(Vector(speed, 0))
        self.environment.selected_entity.rigid_body.movement_properties.velocity += Vector(speed, 0)
        self.draw()

    def move_left(self, key):
        # self.environment.selected_entity.rigid_body.move(Vector(-speed, 0))
        self.environment.selected_entity.rigid_body.movement_properties.velocity += Vector(-speed, 0)
        self.draw()

    def next_selection(self, key):
        self.environment.select_next_entity()
        self.draw()

    def game_loop(self):
        FPS = 60
        SPF = 60 / FPS
        last_time = time.time()
        delta_time = 0
        while True:
            current_time = time.time()
            current_delta = current_time - last_time
            self.environment.integrate(current_delta)
            delta_time = delta_time + current_delta
            last_time = current_time
            if SPF <= delta_time:
                delta_time = 0

            self.resolve_collisions()
            self.draw_hitboxes()
            self.root.update()

    def __init__(self, environment: Environment, is_debugging=True):
        self.is_debugging = is_debugging
        self.environment = environment
        self.root = Tk()
        self.canvas = Canvas(width=500, height=400)

        self.collision_renderer = TkinterCollisionRenderer(self.canvas)
        self.hitbox_renderer = TkinterHitboxRenderer(self.canvas)

        self.root.bind('w', self.move_up)
        self.root.bind('a', self.move_left)
        self.root.bind('s', self.move_down)
        self.root.bind('d', self.move_right)
        self.root.bind('t', self.next_selection)
        self.root.bind('e', self.rotate_right)
        self.root.bind('q', self.rotate_left)

        self.collision_detector = EfficientSATCollisionDetector()
        self.collision_resolver = SimpleCollisionResolver()
        self.physical_collision_resolver = PhysicalCollisionResolver()

        self.canvas.pack()
        self.game_loop()
        self.draw()

    def draw_hitboxes(self):
        self.canvas.delete("all")
        if self.is_debugging:
            for entity in self.environment.physical_entities:
                selected = entity is self.environment.selected_entity
                self.hitbox_renderer.render(entity.rigid_body.get_hitbox(), selected=selected)

    def draw(self):
        self.canvas.delete("all")

        self.resolve_collisions()

        self.root.update()

    def resolve_collisions(self):
        for i in range(1):
            for (a, b) in itertools.product(self.environment.physical_entities, repeat=2):
                if a is b:
                    continue
                r_a = a.rigid_body
                r_b = b.rigid_body

                h_a = r_a.get_hitbox()
                h_b = r_b.get_hitbox()

                collision = None

                if isinstance(h_a, PolygonHitbox) and isinstance(h_b, PolygonHitbox):
                    collision = self.collision_detector.polygon_polygon_collision(h_a.polygon, h_b.polygon)

                elif isinstance(h_a, PolygonHitbox) and isinstance(h_b, CircleHitbox):
                    collision = self.collision_detector.circle_polygon_collision(h_b.circle, h_a.polygon)

                elif isinstance(h_a, CircleHitbox) and isinstance(h_b, PolygonHitbox):
                    collision = self.collision_detector.circle_polygon_collision(h_a.circle, h_b.polygon)

                elif isinstance(h_a, CircleHitbox) and isinstance(h_b, CircleHitbox):
                    collision = self.collision_detector.circle_circle_collision(h_a.circle, h_b.circle)
                self.collision_renderer.render(collision)

                if collision is not None:
                    self.collision_resolver.resolve_collision(r_a, r_b, collision)
                    self.physical_collision_resolver.resolve_collision(r_a, r_b, collision)


class HitboxRenderer:

    def render(self, hitbox: Hitbox):
        pass

    def render_polygon_hitbox(self, polygon_hitbox: PolygonHitbox):
        pass

    def render_circle_hitbox(self, circle_hitbox: CircleHitbox):
        pass


class CollisionRenderer:

    def render(self, collision: Collision):
        pass


class TkinterCollisionRenderer:

    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def render(self, collision: Collision):
        if collision is not None:
            start = collision.start
            end = start + collision.normal.scaled(-collision.depth)
            self.canvas.create_line(start.x, start.y, end.x, end.y, width=2)


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

    def render_circle_hitbox(self, circle_hitbox: CircleHitbox, **kwargs):
        circle = circle_hitbox.circle
        x_start = circle.position.x - circle.radius
        y_start = circle.position.y - circle.radius
        x_end = circle.position.x + circle.radius
        y_end = circle.position.y + circle.radius

        color = 'red' if kwargs.get('selected', False) else 'black'

        self.canvas.create_oval(x_start, y_start, x_end, y_end, outline=color)
        self.canvas.create_oval(circle.position.x - 1, circle.position.y - 1, circle.position.x + 1,
                                circle.position.y + 1)
