from model.component.physical_component import physical_component
from model.component.mental_component import mental_component
from model.component.spiritual_component import spiritual_component

class Entity:
    def __init__(self, sprite, x, y, world, type):
        # set local data and references
        self.world = world
        self.type = type
        self.name = "TestName"

        # Initialize physical component
        self.physical = physical_component(sprite, x, y, self, type)

        # Initialize mental and spiritual components if not an item
        # TODO: this logic should be more dynamic, hard coding "agent" is bad
        if type == "agent":
            self.mental = mental_component(self, type)
            self.spiritual = spiritual_component(self, type)

    # Iterates through all components and updates them, equal to one step through the game loop
    def update(self):
        self.physical.physical_system.update()

        # TODO: this logic should be more dynamic, hard coding "agent" is bad
        if self.type == "agent":
            self.mental.mental_system.update()
            self.spiritual.update()