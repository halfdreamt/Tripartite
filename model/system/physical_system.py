class physical_system:
    def __init__(self, physical_component):
        # set local references
        self.physical = physical_component
        self.world = physical_component.entity.world
        self.entity = physical_component.entity

    # perform checks and such
    def update(self):
        if self.entity.physical.alive:
            if self.physical.life.health <= 0:
                self.die()

            if self.world.isAdjacentToItem(self.physical.xcoord, self.physical.ycoord, "water"):
                self.physical.life.thirst = 100
            elif self.physical.life.thirst > 0:
                self.physical.life.thirst -= 1

            if self.physical.life.thirst <= 0 and self.physical.life.health > 0:
                self.physical.life.health -= 1

            # if self.physical.thirst <= 10:
                    # TODO: add search for water logic
                
            if self.physical.life.moveVectorStack:
                dx, dy = self.physical.life.moveVectorStack.pop()
                self.physical.setLocation(self.physical.xcoord + dx, self.physical.ycoord + dy)
    
    def die(self):
        self.health = 0