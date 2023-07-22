class renderSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, oldValue=None, newValue=None):
        if component.get_name() == "render":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        for entity in self.entities:
            if entity.has_component('position') and entity.has_component('render'):
                # Update map layer based on the render component's map name (might require specifying the map container name in the render component as well)
                # Actually, an "active" update system might be worse than a "passive" system which leverages my existing component update system (not sure if I'm even using that anywhere, but this an ideal case)
                pass

    def reset_system(self):
        self.entities = []