class battleSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, oldValue=None, newValue=None):
        if component.get_name() == "battle_position":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        pass

    def reset_system(self):
        self.entities = []