class movementSystem:
    def __init__(self):
        self.entities = []

    def component_updated(self, component):
        if component.get_name() == "movement":
            self.entities.append(component.entity)

    def update(self):
        for entity in self.entities:
            if entity.get_component_data("movement", "state") == "moving":
                self.move(entity)

    def move(self, entity):
        entity.update_component_data("position", "x", entity.get_component_data("position", "x") + entity.get_component_data("movement", "xVel"))
        entity.update_component_data("position", "y", entity.get_component_data("position", "y") + entity.get_component_data("movement", "yVel"))