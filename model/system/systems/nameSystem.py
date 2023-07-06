class nameSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "name":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        pass

    def get_name(self, entity):
        return entity.get_component_data("name", "name")
    
    def set_name(self, entity, name):
        entity.update_component_data("name", "name", name)

    def reset_system(self):
        self.entities = []
