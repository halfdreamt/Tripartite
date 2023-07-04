class collisionSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    # TODO: Noticed an issue with collision, possibly isolated to when following a path
    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "collision":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def check_collision(self, entity):
        world = entity.get_world()
        position = self.system_manager.get_system("position").get_position(entity)
        return world.map.get_valid_moves(position[0], position[1])

    def update(self):
        pass