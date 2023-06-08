import random

class wanderSystem:
    def __init__(self):
        self.entities = []

    def component_updated(self, component):
        if component.get_name() == "wander":
            self.entities.append(component.entity)

    def update(self):
        for entity in self.entities:
            if entity.get_component_data("movement", "state") == "idle" and entity.get_component_data("wander", "active"):
                self.wander(entity)

    #Queries the entity's world's map for valid tiles to move to and picks a random one to set movement to
    def wander(self, entity):
        world = entity.get_world()
        x = entity.get_component_data("position", "x")
        y = entity.get_component_data("position", "y")
        validMoves = world.map.getValidMoves(x, y)
        if len(validMoves) > 0:
            moves = random.choice(validMoves)
            movesList = moves.split(",")
            movex = int(movesList[0])
            movey = int(movesList[1])
            entity.update_component_data("movement", "xVel", movex)
            entity.update_component_data("movement", "yVel", movey)
            entity.update_component_data("movement", "state", "moving")