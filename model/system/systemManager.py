from model.system.wanderSystem import wanderSystem
from model.system.movementSystem import movementSystem

class SystemManager:
    def __init__(self):
        self.systems = []
        self.add_system(wanderSystem())
        self.add_system(movementSystem())

    def update_systems(self):
        for system in self.systems:
            system.update()

    def add_system(self, system):
        self.systems.append(system)

    def return_systems(self):
        return self.systems
    
    def component_updated(self, component, updateType):
        for system in self.systems:
            system.component_updated(component)