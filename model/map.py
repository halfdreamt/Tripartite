from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Map:
    def __init__(self, map_data):
        # Initialize the map layers
        self.layers = {}

        #set map data
        self.TILESIZE, self.MAPWIDTH, self.MAPHEIGHT = map_data['tilewidth'], map_data['width'], map_data['height']

        # Load the layers from the map data
        for layer in map_data['layers']:
            layer_data = layer['data']
            # Convert the 1D array into a 2D array
            layer_data_2D = [layer_data[i*self.MAPWIDTH:(i+1)*self.MAPWIDTH] for i in range(self.MAPHEIGHT)]
            self.layers[layer['name']] = layer_data_2D

    #returns all non-zero tile ids in the given layer, along with their locations
    def getLayerIds(self, layerName):
        layer_data = self.layers.get(layerName, [])
        ids = []
        for y in range(self.MAPHEIGHT):
            for x in range(self.MAPWIDTH):
                if layer_data[y][x] != 0:
                    ids.append((layer_data[y][x], x, y))
        return ids
            
    #returns the tile id at the given location
    def getLayerId(self, layerName, x, y): 
        layer_data = self.layers.get(layerName, [])
        if layer_data and 0 <= x < self.MAPWIDTH and 0 <= y < self.MAPHEIGHT:
            return layer_data[y][x]
        return 0

    #returns the collision layer where all 0 values are 1, and all non-zero values are 0
    def getCollisionLayer(self):
        collision_layer = []
        for y in range(self.MAPHEIGHT):
            collision_layer.append([])
            for x in range(self.MAPWIDTH):
                collision_layer[y].append(0 if self.getLayerId('collision', x, y) == 0 else 1)
        return collision_layer
    
    # converts a path of nodes to a list of move directions
    def pathToDirections(self, path):
        directions = []
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            directions.append(str(x2 - x1) + " , " + str(y2 - y1))
        return directions
    
    #returns an array of move directions which represent a path from the start to the end
    def getPath(self, start, end):
        grid = Grid(matrix=self.getCollisionLayer())
        start = grid.node(start[0], start[1])
        end = grid.node(end[0], end[1])
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)
        return path

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
            valid_directions.append((0 , -1))
        if y < self.MAPHEIGHT - 1 and not self.hasCollision(x, y + 1):
            valid_directions.append((0 , 1))
        if x > 0 and not self.hasCollision(x - 1, y):
            valid_directions.append((-1 , 0))
        if x < self.MAPWIDTH - 1 and not self.hasCollision(x + 1, y):
            valid_directions.append((1 , 0))
        return valid_directions

    # iterates through all entities and updates them, equal to one step through the game loop
    def updateMap(self, entities):
        self.updateLayer("sprites", entities)

    # updates the given layer with the given values and positions
    def updateLayer(self, layerName, entities):
        #clear layer
        for y in range(self.MAPHEIGHT):
            for x in range(self.MAPWIDTH):
                self.setLayerId(layerName, x, y, 0)
        for entity in entities:
            self.setLayerId('sprites', entity.get_component_data('position', 'x'), entity.get_component_data('position', 'y'), entity.get_component_data('render', 'spriteID'))
