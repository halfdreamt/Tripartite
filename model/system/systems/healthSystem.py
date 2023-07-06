class healthSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "physical_health":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        pass

    def damage(self, entity, amount, source, type):
        entity.update_component_data("physical_health", "current", entity.get_component_data("physical_health", "current") - amount)

    def reset_system(self):
        self.entities = []
