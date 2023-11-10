from entity import *


class GameEnvironment:

    def __init__(self, physical_entities: list[PhysicalEntity]):
        self.physical_entities = physical_entities
        self.selected_entity = physical_entities[0]

