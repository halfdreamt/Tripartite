from model.system.physical_system import physical_system

class physical_component:
    def __init__(self, sprite, x, y, entity, type):
        self.xcoord = x
        self.ycoord = y
        self.alive = True
        self.sprite = sprite
        self.entity = entity
        self.health = 20
        self.physical_system = physical_system(self)

        if type == "item":
            self.alive = False