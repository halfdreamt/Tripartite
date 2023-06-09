class movementSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, value=None):
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

    def set_movement(self, entity, xVel, yVel):
        entity.update_component_data("movement", "xVel", xVel)
        entity.update_component_data("movement", "yVel", yVel)

    def move(self, entity):
        entity.update_component_data("position", "x", entity.get_component_data("position", "x") + entity.get_component_data("movement", "xVel"))
        entity.update_component_data("position", "y", entity.get_component_data("position", "y") + entity.get_component_data("movement", "yVel"))
        entity.update_component_data("movement", "xVel", 0)
        entity.update_component_data("movement", "yVel", 0)