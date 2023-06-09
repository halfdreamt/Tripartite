from model.system.wanderSystem import wanderSystem
from model.system.movementSystem import movementSystem
from model.system.thirstSystem import thirstSystem
from model.system.healthSystem import healthSystem
from model.system.collisionSystem import collisionSystem
from model.system.pathfindingSystem import pathfindingSystem
from model.system.positionSystem import positionSystem
from model.system.needsSystem import needsSystem

class SystemManager:
    def __init__(self):
        self.systems = []
        self.add_system(wanderSystem(len(self.systems), "wander", self))
        self.add_system(movementSystem(len(self.systems), "movement", self))
        self.add_system(thirstSystem(len(self.systems), "thirst", self))
        self.add_system(healthSystem(len(self.systems), "health", self))
        self.add_system(collisionSystem(len(self.systems), "collision", self))
        self.add_system(pathfindingSystem(len(self.systems), "pathfinding", self))
        self.add_system(positionSystem(len(self.systems), "position", self))
        self.add_system(needsSystem(len(self.systems), "needs", self))

    def update_systems(self):
        for system in self.systems:
            system.update()

    def add_system(self, system):
        self.systems.append(system)

    def return_systems(self):
        return self.systems
    
    def get_system(self, name):
        for system in self.systems:
            if system.name == name:
                return system
    
    def component_updated(self, component, updateType, key=None, value=None):
        for system in self.systems:
            system.component_updated(component, updateType, key, value)