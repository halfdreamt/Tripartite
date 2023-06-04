from model.system.physical_system import physical_system

class physical_component:
    def __init__(self, sprite, x, y, entity, type):

        # set local data and references - in this case, the physical component is aware of the entity it belongs to and its location, and the sprite it should be drawn with
        self.xcoord = x
        self.ycoord = y
        self.alive = True
        self.sprite = sprite
        self.entity = entity
        self.moveDirection = None
        self.pendingMove = False
        self.map = entity.world.map

        # Set health - TODO: this should be dynamic, not hard coded
        self.health = 20

        # initialize physical system; behavior
        self.physical_system = physical_system(self)

        # Set certain properties based on type - TODO: this should be dynamic, not hard coded
        if type == "item":
            self.alive = False

    def setMoveDirection(self, x, y):
        if not self.map.hasCollision(self.xcoord + x, self.ycoord + y):
            self.moveDirection = (x, y)
            self.pendingMove = True
            return True
        else:
            return False