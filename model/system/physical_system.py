class physical_system:
    def __init__(self, physical_component):
        # set local references
        self.physical = physical_component
        self.world = physical_component.entity.world
        self.entity = physical_component.entity

    # perform checks and such
    def update(self):
        if self.entity.type == "agent":
            if self.physical.alive.health <= 0:
                self.die()

            if self.world.isAdjacentToItem(self.physical.xcoord, self.physical.ycoord, "water"):
                self.physical.alive.thirst = 100
            elif self.physical.alive.thirst > 0:
                self.physical.alive.thirst -= 1

            if self.physical.alive.thirst <= 0 and self.physical.alive.health > 0:
                self.physical.alive.health -= 1

            # if self.physical.thirst <= 10:
                    # TODO: add search for water logic
                
            if self.physical.alive.moveVectorStack:
                dx, dy = self.physical.alive.moveVectorStack.pop()
                self.physical.setLocation(self.physical.xcoord + dx, self.physical.ycoord + dy)
    
    def die(self):
        self.health = 0