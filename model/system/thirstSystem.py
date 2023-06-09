class thirstSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType):
        if component.get_name() == "thirst" or component.get_name() == "drinkable":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        for entity in self.entities:
            if entity.has_component("thirst"):
                self.thirst(entity)

    def thirst(self, entity):
        if entity.get_component_data("thirst", "current") > 0:
            entity.update_component_data("thirst", "current", entity.get_component_data("thirst", "current") - 1)
        else:
            for system in self.system_manager.return_systems():
                if system.name == "health":
                    system.damage(entity, 1, self.name, "thirst")
                    break
