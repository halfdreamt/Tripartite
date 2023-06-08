from model.system.wanderSystem import wanderSystem
from model.system.movementSystem import movementSystem
from model.system.thirstSystem import thirstSystem
from model.system.healthSystem import healthSystem

class SystemManager:
    def __init__(self):
        self.systems = []
        self.add_system(wanderSystem(len(self.systems), "wander", self))
        self.add_system(movementSystem(len(self.systems), "movement", self))
        self.add_system(thirstSystem(len(self.systems), "thirst", self))
        self.add_system(healthSystem(len(self.systems), "health", self))

    def update_systems(self):
        for system in self.systems:
            system.update()

    def add_system(self, system):
        self.systems.append(system)

    def return_systems(self):
        return self.systems
    
    def component_updated(self, component, updateType):
        for system in self.systems:
            system.component_updated(component, updateType)