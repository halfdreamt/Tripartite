from model.system.physical_system import physical_system

class physical_component:
    def __init__(self, sprite, x, y, entity, type):

        # set local data and references - in this case, the physical component is aware of the entity it belongs to and its location, and the sprite it should be drawn with
        self.xcoord = x
        self.ycoord = y
        self.sprite = sprite
        self.entity = entity
        self.map = entity.world.map
        
        self.alive = True

        # Set health - TODO: this should be dynamic, not hard coded
        self.health = 20

        # initialize physical system; behavior
        self.physical_system = physical_system(self)

        # Set certain properties based on type - TODO: this should be dynamic, not hard coded
        if type == "item":
            self.alive = False

    # sets relative movement direction
    def setMoveVector(self, x, y):
        if not self.map.hasCollision(self.xcoord + x, self.ycoord + y):
            self.xcoord += x
            self.ycoord += y
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