class movementSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, oldValue=None, newValue=None):
        if component.get_name() == "movement":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        for entity in self.entities:
            if entity.get_component_data("movement", "xVel") != 0 or entity.get_component_data("movement", "yVel") != 0:
                self.move(entity)

    def set_movement(self, entity, xVel, yVel, source):
        position = self.system_manager.get_system("position").get_position(entity)
        validMoves = entity.world.map.get_valid_moves(position[0], position[1])
        if (xVel, yVel) in validMoves:
            entity.update_component_data("movement", "xVel", xVel)
            entity.update_component_data("movement", "yVel", yVel)
            return True
        else:
            print("Invalid move for " + entity.get_component_data("name", "name") + " by " + str(source) + " to " + str(position[0] + xVel) + ", " + str(position[1] + yVel) + ". Reason: Collision")
            return False

    def move(self, entity):
        position = self.system_manager.get_system("position").get_position(entity)
        self.system_manager.get_system("position").set_position(entity, position[0] + entity.get_component_data("movement", "xVel"), position[1] + entity.get_component_data("movement", "yVel"))
        entity.update_component_data("movement", "xVel", 0)
        entity.update_component_data("movement", "yVel", 0)

    def reset_system(self):
        self.entities = []