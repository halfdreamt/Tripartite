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

    def isNearWater(self, entity):
        x = entity.get_component_data("position", "x")
        y = entity.get_component_data("position", "y")
        for i in range(-1, 2):
            for j in range(-1, 2):
                world = entity.get_world()
                waterEntity = world.entity_manager.get_entity_at(x + i, y + j)
                if waterEntity:
                    if waterEntity.has_component("drinkable"):
                        return True
        return False

    def update(self):
        for entity in self.entities:
            if entity.has_component("thirst"):
                self.thirst(entity)
                self.hydrate(entity)

    def thirst(self, entity):
        if entity.get_component_data("thirst", "current") > 0:
            entity.update_component_data("thirst", "current", entity.get_component_data("thirst", "current") - 1)
            if entity.get_component_data("thirst", "current") < 10:
                if entity.get_component_data("thirst", "state") != "thirsty":
                    entity.update_component_data("thirst", "state", "thirsty")
                    self.system_manager.get_system("needs").add_need(entity, "thirst", 1)
        else:
            system = self.system_manager.get_system("health")
            system.damage(entity, 1, self.name, "thirst")

    def hydrate(self, entity):
        if self.isNearWater(entity):
            entity.update_component_data("thirst", "current", entity.get_component_data("thirst", "max"))
            entity.update_component_data("thirst", "state", "hydrated")
            if self.system_manager.get_system("needs").has_need(entity, "thirst"):
                self.system_manager.get_system("needs").remove_need(entity, "thirst")