class movementSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType):
        if component.get_name() == "movement" and updateType == "create":
            self.entities.append(component.entity)

    def update(self):
        for entity in self.entities:
            if entity.get_component_data("movement", "state") == "moving":
                self.move(entity)

    def move(self, entity):
        entity.update_component_data("position", "x", entity.get_component_data("position", "x") + entity.get_component_data("movement", "xVel"))
        entity.update_component_data("position", "y", entity.get_component_data("position", "y") + entity.get_component_data("movement", "yVel"))
        entity.update_component_data("movement", "state", "idle")