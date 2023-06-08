class SystemManager:
    def __init__(self):
        self.systems = []

    def update_systems(self):
        for system in self.systems:
            system.update()

    def return_systems(self):
        return self.systems
    
    def component_updated(self, component, updateType):
        for system in self.systems:
            system.component_updated(component)