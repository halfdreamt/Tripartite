from model.system.physical_system import physical_system

class physical_component:
    def __init__(self, sprite, x, y, entity, alive, health, thirst):

        # set local data and references - in this case, the physical component is aware of the entity it belongs to and its location, and the sprite it should be drawn with
        self.xcoord = x
        self.ycoord = y
        self.sprite = sprite
        self.entity = entity
        self.map = entity.world.map
        self.alive = alive        
        self.moveVectorStack = []
        self.health = health
        self.thirst = thirst
    
        # initialize physical system; behavior
        self.physical_system = physical_system(self)

     # sets relative movement direction
    def pushMoveVector(self, x, y):
        if not self.map.hasCollision(self.xcoord + x, self.ycoord + y):
            self.moveVectorStack.append((x, y))
            return True
        else:
            return False
        
    # sets absolute location
    def setLocation(self, x, y):
        if not self.map.hasCollision(x, y):
            self.xcoord = x
            self.ycoord = y
            return True
        else:
            return False