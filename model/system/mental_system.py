import random

class mental_system:
    def __init__(self, mental_component):
        self.mental = mental_component
        self.world = mental_component.entity.world
        self.entity = mental_component.entity

    def wander(self): 
            valid_directions = self.world.map.getValidMoves(self.entity.physical.xcoord, self.entity.physical.ycoord)
            
            if valid_directions:
                coords_list = random.choice(valid_directions).split(",")
                xcoord = int(coords_list[0])
                ycoord = int(coords_list[1])
                self.mental.setMoveDirection(xcoord, ycoord)

            self.entity.physical.physical_system.move()

    def update(self):
        if self.mental.willWander and not self.mental.pendingMove:
                self.wander()