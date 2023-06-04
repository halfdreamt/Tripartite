class physical_system:
    def __init__(self, physical_component):
        # set local references
        self.physical = physical_component
        self.world = physical_component.entity.world
        self.entity = physical_component.entity

    # perform checks and such
    def update(self):
        if self.entity.physical.alive:
            if self.physical.health <= 0:
                self.die()

            self.manageWater()
                
            if self.physical.moveVectorStack:
                dx, dy = self.physical.moveVectorStack.pop()
                self.physical.setLocation(self.physical.xcoord + dx, self.physical.ycoord + dy)
    
    def die(self):
        self.health = 0

    def manageWater(self):
        if self.world.isAdjacentToItem(self.physical.xcoord, self.physical.ycoord, "water"):
            self.physical.thirst = 100
        elif self.physical.thirst > 0:
            self.physical.thirst -= 1

        if self.physical.thirst <= 0 and self.physical.health > 0:
            self.physical.health -= 1