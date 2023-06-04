import random

# Mental System
class mental_system:
    def __init__(self, mental_component):
        # set local references
        self.mental = mental_component
        self.world = mental_component.entity.world
        self.entity = mental_component.entity
        self.physical = mental_component.entity.physical

    # Sets a valid random move direction
    def wander(self): 
        valid_directions = self.world.map.getValidMoves(self.entity.physical.xcoord, self.entity.physical.ycoord)
        
        if valid_directions:
            coords_list = random.choice(valid_directions).split(",")
            xcoord = int(coords_list[0])
            ycoord = int(coords_list[1])
            self.physical.pushMoveVector(xcoord, ycoord)

    # Update the mental system
    def update(self):
        if self.mental.willWander:
            self.wander()