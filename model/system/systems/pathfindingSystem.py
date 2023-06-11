class pathfindingSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "pathfinding":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def get_reason(self, entity):
        return entity.get_component_data("pathfinding", "reason")

    def next_move(self, entity):
        curDirections = entity.get_component_data("pathfinding", "directions") 
        if self.system_manager.get_system("movement").set_movement(entity, curDirections[0][0], curDirections[0][1], "pathfindingSystem"):
            entity.update_component_data("pathfinding", "directions", curDirections[1:])
        else:
            self.set_path(entity, entity.get_component_data("pathfinding", "reason"), entity.get_component_data("pathfinding", "destinationX"), entity.get_component_data("pathfinding", "destinationY"))

    def get_path(self, entity, targetX , targetY):
        position = self.system_manager.get_system("position").get_position(entity)
        path = entity.world.map.get_path((position[0], position[1]), (targetX, targetY))
        return path
    
    def set_path(self, entity, reason, targetX, targetY):
        # TODO: Return false if no path found
        path = self.get_path(entity, targetX, targetY)
        directions = entity.world.map.pathToDirections(path)
        entity.update_component_data("pathfinding", "directions", directions)
        entity.update_component_data("pathfinding", "path", path)
        entity.update_component_data("pathfinding", "reason", reason)
        entity.update_component_data("pathfinding", "destinationX", targetX)
        entity.update_component_data("pathfinding", "destinationY", targetY)
        entity.update_component_data("wander", "active", False)

    def clear_path(self, entity):
        entity.update_component_data("pathfinding", "directions", [])
        entity.update_component_data("pathfinding", "reason", "none")
        entity.update_component_data("pathfinding", "path", [])
        entity.update_component_data("pathfinding", "destinationX", -1)
        entity.update_component_data("pathfinding", "destinationY", -1)
        entity.update_component_data("wander", "active", True)

    def update(self):
        for entity in self.entities:
            if entity.get_component_data("pathfinding", "reason") != "none":
                if len(entity.get_component_data("pathfinding", "directions")) > 0:
                    self.next_move(entity)
                else:
                    self.clear_path(entity)