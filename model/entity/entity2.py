class Entity:
    def __init__(self, id, systems):
        self.id = id
        self.components = {}
        self.systems = systems  # Reference to all systems

    def add_component(self, component):
        self.components[type(component).__name__] = component
        self.notify_systems()

    def remove_component(self, component_type):
        if component_type in self.components:
            del self.components[component_type]
        self.notify_systems()

    def get_component(self, component_type):
        return self.components[component_type]
    
    def has_component(self, component_type):
        return component_type in self.components
    
    def get_component_info(self, component_type):
        return self.components[component_type].get_info()

    def notify_systems(self):
        for system in self.systems:
            system.entity_updated(self)