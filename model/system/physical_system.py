class physical_system:
    def __init__(self, physical_component):
        # set local references
        self.physical = physical_component
        self.world = physical_component.entity.world
        self.entity = physical_component.entity

    # finalizes the move, assuming collision has been checked (TODO: this should be moved to the map class, maybe? Per the AI's suggestion, though I might want to add validation here as well)
    def move(self):
        if self.physical.pendingMove:
            dx, dy = self.physical.moveDirection
            next_x, next_y = self.physical.xcoord + dx, self.physical.ycoord + dy

            self.physical.xcoord = next_x
            self.physical.ycoord = next_y
            self.physical.pendingMove = False

    # perform checks and such
    def update(self):
        if self.physical.health <= 0:
            self.die()
    
    def die(self):
        self.health = 0