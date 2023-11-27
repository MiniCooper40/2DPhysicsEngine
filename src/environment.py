from entity import *


class Environment:

    def select_next_entity(self):
        if self.selected_index == len(self.physical_entities)-1:
            self.selected_index = 0
        else:
            self.selected_index += 1
        self.selected_entity = self.physical_entities[self.selected_index]

    def __init__(self, physical_entities: list[PhysicalEntity]):
        self.physical_entities = physical_entities
        self.selected_index = 0
        self.selected_entity = physical_entities[0]

    def integrate(self, delta_time):
        for physical_entity in self.physical_entities:
            physical_entity.rigid_body.move(physical_entity.rigid_body.movement_properties.integrate_position(delta_time))
            physical_entity.rigid_body.rotate(physical_entity.rigid_body.movement_properties.integrate_rotate(delta_time))
            physical_entity.rigid_body.movement_properties.integrate(delta_time)

