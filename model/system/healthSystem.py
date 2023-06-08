class healthSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType):
        if component.get_name() == "health" and updateType == "create":
            self.entities.append(component.entity)

    def update(self):
        pass

    def damage(self, entity, amount, source, type):
        entity.update_component_data("health", "current", entity.get_component_data("health", "current") - amount)
