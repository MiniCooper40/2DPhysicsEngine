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

