import random

class wanderSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType):
        if component.get_name() == "wander":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        for entity in self.entities:
            if entity.get_component_data("movement", "state") == "idle" and entity.get_component_data("wander", "active"):
                self.wander(entity)

    #Queries the entity's world's map for valid tiles to move to and picks a random one to set movement to
    def wander(self, entity):
        x = entity.get_component_data("position", "x")
        y = entity.get_component_data("position", "y")
        system = self.system_manager.get_system("collision")
        validMoves = system.check_collision(entity)
        if len(validMoves) > 0:
            moves = random.choice(validMoves)
            self.system_manager.get_system("movement").set_movement(entity, moves[0], moves[1])