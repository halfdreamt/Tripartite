from model.entity.map import Map
from model.entity.entity import Entity

class World:
    def __init__(self, map_data):
        self.map = Map(map_data)
        self.time = 0
        self.TILESIZE = self.map.TILESIZE
        self.entities = self.create_entities(map_data)

    def create_entities(self, map_data):
        entities = []
        for layer in map_data['layers']:
            if layer['name'] == 'sprites':
                sprites = layer['data']
                for y in range(self.map.MAPHEIGHT):
                    for x in range(self.map.MAPWIDTH):
                        sprite = sprites[y * self.map.MAPWIDTH + x]
                        if sprite != 0:
                            entity = Entity(sprite, x, y, self, "agent")
                            entities.append(entity)
            if layer['name'] == 'items':
                sprites = layer['data']
                for y in range(self.map.MAPHEIGHT):
                    for x in range(self.map.MAPWIDTH):
                        sprite = sprites[y * self.map.MAPWIDTH + x]
                        if sprite != 0:
                            entity = Entity(sprite, x, y, self, "item")
                            entities.append(entity)
        return entities

    def getEntityInfo(self, x, y):
        for entity in self.entities:
            if entity.physical.xcoord == x and entity.physical.ycoord == y:
                return entity
        return None

    def tick(self, ):
        for entitiy in self.entities:
            entitiy.update()
        self.incrementTime()
        self.map.updateMap(self.entities)

    def incrementTime(self):
        self.time += 1