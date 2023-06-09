class pathfindingSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType):
        if component.get_name() == "pathfinding":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def next_move(self, entity):
        curDirections = entity.get_component_data("pathfinding", "directions")
        # TODO: run a collision check here, recalculate path if necessary
        self.system_manager.get_system("movement").set_movement(entity, curDirections[0][0], curDirections[0][1])
        entity.update_component_data("pathfinding", "directions", curDirections[1:])

    def get_path(self, entity, target):
        x = entity.get_component_data("position", "x")
        y = entity.get_component_data("position", "y")
        targetX = target.get_component_data("position", "x")
        targetY = target.get_component_data("position", "y")
        world = entity.get_world()
        path = world.map.get_path((x, y), (targetX, targetY))
        return world.map.pathToDirections(path)

    def update(self):
        for entity in self.entities:
            if entity.get_component_data("movement", "state") == "pathing":
                if len(entity.get_component_data("pathfinding", "directions")):
                    self.next_move(entity)
                else:
                    entity.update_component_data("movement", "state", "idle")