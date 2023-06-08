from model.map import Map
from model.entity.entityManager import EntityManager
from model.component.componentManager import ComponentManager

# The World class is another name for gamestate. It contains the map, the time, and the entities.
class World:
    def __init__(self, map_data):
        # Initialize the map
        self.map = Map(map_data)

        # Initialize the time
        self.time = 0

        # Initialize the entities
        self.component_manager = ComponentManager('rec/components.json', [])
        spriteData = self.map.getLayerIds('sprites')
        self.entity_manager = EntityManager('rec/entities.json', self.component_manager, spriteData)

    # Returns the entity at the given location
    def getEntityInfo(self, x, y):
        for entity in self.entities:
            if entity.physical.xcoord == x and entity.physical.ycoord == y:
                return entity
        return None
    
    def isAdjacentToItem(self, x, y, itemName):
        items = self.getEntityByName(itemName)
        if items:
            for item in items:
                if abs(item.physical.xcoord - x) + abs(item.physical.ycoord - y) == 1:
                    return True
        return False
    
    # Returns all entities of the given name
    def getEntityByName(self, name):
        entities = []
        for entity in self.entities:
            if entity.name == name:
                entities.append(entity)
        return entities

    # Iterates through all entities and updates them, equal to one step through the game loop
    def tick(self):
        for entity in self.entities:
            entity.update()
        self.incrementTime()
        self.map.updateMap(self.entities)

    # Increments the time
    def incrementTime(self):
        self.time += 1