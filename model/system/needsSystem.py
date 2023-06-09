class needsSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "needs":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def add_need(self, entity, name, priority):
        entity.update_component_data("needs", "needs", entity.get_component_data("needs", "needs") + [(name, priority)])

    def remove_need(self, entity, need):
        entity.update_component_data("needs", "needs", [x for x in entity.get_component_data("needs", "needs") if x != need])

    def get_highest_priority_need(self, entity):
        if len(entity.get_component_data("needs", "needs")) == 0:
            return None
        highest = entity.get_component_data("needs", "needs")[0]
        for need in entity.get_component_data("needs", "needs"):
            if need[1] > highest[1]:
                highest = need
        return highest

    def has_need(self, entity, need):
        return need in entity.get_component_data("needs", "needs")

    def update(self):
        for entity in self.entities:
            highestNeed = self.get_highest_priority_need(entity)
            if highestNeed != None and highestNeed[0] == "thirst":
                nearestWater = self.system_manager.get_system("position").get_nearest_entity(entity, "Water Pot")
                waterX = nearestWater.get_component_data("position", "x")
                waterY = nearestWater.get_component_data("position", "y")
                spotNextToWater = entity.world.map.getRandomValidMove(waterX, waterY)
                self.system_manager.get_system("pathfinding").set_path(entity, spotNextToWater[0] + waterX, spotNextToWater[1] + waterY)
