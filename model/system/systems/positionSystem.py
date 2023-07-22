from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class positionSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []

    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "position":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                #should change this to update the render component upon position change, which should update the map entity with the change
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def get_nearest_entity(self, entity, name):
        entities = entity.world.entity_manager.get_entities_by_name(name)
        if not len(entities):
            return None
        nearest = entities[0]
        nearestDist = self.get_distance(entity, nearest)
        for other in entities:
            dist = self.get_distance(entity, other)
            if dist < nearestDist:
                nearest = other
                nearestDist = dist
        return nearest
    
    def get_position(self, entity):
        return (entity.get_component_data("position", "x"), entity.get_component_data("position", "y"))
    
    def set_position(self, entity, x, y):
        entity.update_component_data("position", "x", x)
        entity.update_component_data("position", "y", y)
    
    def get_distance(self, entity1, entity2):
        x1 = entity1.get_component_data("position", "x")
        y1 = entity1.get_component_data("position", "y")
        x2 = entity2.get_component_data("position", "x")
        y2 = entity2.get_component_data("position", "y")
        return abs(x1 - x2) + abs(y1 - y2)

    def update(self):
        pass

    def reset_system(self):
        self.entities = []