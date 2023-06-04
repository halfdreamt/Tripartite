from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Map:
    def __init__(self, map_data):
        self.layers = {}
        self.TILESIZE, self.MAPWIDTH, self.MAPHEIGHT = map_data['tilewidth'], map_data['width'], map_data['height']

        for layer in map_data['layers']:
            layer_data = layer['data']
            # Convert the 1D array into a 2D array
            layer_data_2D = [layer_data[i*self.MAPWIDTH:(i+1)*self.MAPWIDTH] for i in range(self.MAPHEIGHT)]
            self.layers[layer['name']] = layer_data_2D
            
    #returns the tile id at the given location
    def getLayerId(self, layerName, x, y): 
        layer_data = self.layers.get(layerName, [])
        if layer_data and 0 <= x < self.MAPWIDTH and 0 <= y < self.MAPHEIGHT:
            return layer_data[y][x]
        return 0
    
    # Returns the number of non-zero tiles in the layer
    def getLayerCount(self, layerName): 
        layer_data = self.layers.get(layerName, [])
        if layer_data:
            return sum([sum([1 for tile in row if tile]) for row in layer_data])
        return 0
    
    # Sets the value of the tile at the given location
    def setLayerId(self, layerName, x, y, value): 
        layer_data = self.layers.get(layerName, [])
        if layer_data and 0 <= x < self.MAPWIDTH and 0 <= y < self.MAPHEIGHT:
            layer_data[y][x] = value

    #returns true if there is a collision at the given location
    def hasCollision(self, x, y): 
        collision_id = self.getLayerId('collision', x, y)
        return collision_id != 0
    
    #returns a list of valid directions to move in
    def getValidMoves(self, x, y): 
        valid_directions = []
        if y > 0 and not self.hasCollision(x, y - 1):
            valid_directions.append("0 , -1")
        if y < self.MAPHEIGHT - 1 and not self.hasCollision(x, y + 1):
            valid_directions.append("0 , 1")
        if x > 0 and not self.hasCollision(x - 1, y):
            valid_directions.append("-1 , 0")
        if x < self.MAPWIDTH - 1 and not self.hasCollision(x + 1, y):
            valid_directions.append("1 , 0")
        return valid_directions
    
    #returns the location of the nearest item of the given type
    def findNearestItem(self, x, y, itemName):
        items = self.findItems(itemName)
        if items:
            item = min(items, key=lambda item: abs(item.physical.xcoord - x) + abs(item.physical.ycoord - y))
            return (item.physical.xcoord, item.physical.ycoord)
        return None

    #Retrieves entity locations and updates the sprites layer
    def updateEntities(self, entities):
        #clear sprites layer
        for y in range(self.MAPHEIGHT):
            for x in range(self.MAPWIDTH):
                self.setLayerId('sprites', x, y, 0)
        for entity in entities:
            self.setLayerId('sprites', entity.physical.xcoord, entity.physical.ycoord, entity.physical.sprite)

    def updateMap(self, entities):
        self.updateEntities(entities)
