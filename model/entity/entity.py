from model.component.physical_component import physical_component
from model.component.mental_component import mental_component
from model.component.spiritual_component import spiritual_component

class Entity:
    def __init__(self, sprite, x, y, world, type):
        self.world = world
        self.sprite = sprite
        self.type = type
        self.name = "TestName"
        self.physical = physical_component(self.sprite, x, y, self, type)

        if type == "agent":
            self.mental = mental_component(self, type)
            self.spiritual = spiritual_component(self, type)

    def update(self):
        self.physical.physical_system.update()

        if self.type == "agent":
            self.mental.mental_system.update()
            self.spiritual.update()