class physical_system:
    def __init__(self, physical_component):
        self.physical = physical_component
        self.world = physical_component.entity.world
        self.entity = physical_component.entity

    def move(self):
        if self.entity.mental.pendingMove:
            dx, dy = self.entity.mental.moveDirection
            next_x, next_y = self.physical.xcoord + dx, self.physical.ycoord + dy

            self.physical.xcoord = next_x
            self.physical.ycoord = next_y
            self.entity.mental.pendingMove = False

    def update(self):
        if self.physical.health <= 0:
            self.die()
    
    def die(self):
        self.health = 0