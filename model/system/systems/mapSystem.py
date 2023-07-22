from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import random

class mapSystem:
    def __init__(self, ID, name, system_manager):
        self.ID = ID
        self.name = name
        self.system_manager = system_manager
        self.entities = []
        self.layers = []

    def component_updated(self, component, updateType, key=None, value=None):
        if component.get_name() == "map_layers":
            if updateType == "create":
                self.entities.append(component.entity)
            elif updateType == "update":
                pass
            elif updateType == "delete":
                self.entities.remove(component.entity)

    def update(self):
        for entity in self.entities:
            self.age(entity)

    def reset_system(self):
        self.entities = []

    def load_map(self, map_data):
        #set map data
        self.TILESIZE, self.MAPWIDTH, self.MAPHEIGHT = map_data['tilesize'], map_data['width'], map_data['height']

        self.name = map_data['name']

        # Load the layers from the map data
        for layer in map_data['layers']:
            layer_data = layer['data']
            # Check if layer data is 1D or 2D
            if isinstance(layer_data[0], int):
                # Convert the 1D array into a 2D array
                layer_data_2D = [layer_data[i*self.MAPWIDTH:(i+1)*self.MAPWIDTH] for i in range(self.MAPHEIGHT)]
                self.layers[layer['name']] = layer_data_2D
            else:
                # Layer data is already 2D
                self.layers[layer['name']] = layer_data

    #returns all non-zero tile ids in the given layer, along with their locations
    def get_layer_ids(self, layerName):
        layer_data = self.layers.get(layerName, [])
        ids = []
        for y in range(self.MAPHEIGHT):
            for x in range(self.MAPWIDTH):
                if layer_data[y][x] != 0:
                    ids.append((layer_data[y][x], x, y))
        return ids
    
    #returns a the tile ID aat the given location, on the given layer
    def get_layer_tile(self, layerName, x, y):
        layer_data = self.layers.get(layerName, [])
        if layer_data and 0 <= x < self.MAPWIDTH and 0 <= y < self.MAPHEIGHT:
            return layer_data[y][x]
        return 0
            
    #returns the tile id at the given location
    def get_layer_id(self, layerName, x, y): 
        layer_data = self.layers.get(layerName, [])
        if layer_data and 0 <= x < self.MAPWIDTH and 0 <= y < self.MAPHEIGHT:
            return layer_data[y][x]
        return 0

    #returns the collision layer where all 0 values are 1, and all non-zero values are 0
    def get_collision_layer(self):
        collision_layer = []
        for y in range(self.MAPHEIGHT):
            collision_layer.append([])
            for x in range(self.MAPWIDTH):
                collision_layer[y].append(1 if self.get_layer_id('collision', x, y) == 0 else 0)
        return collision_layer
    
    # converts a path of nodes to an array of move directions
    def path_to_directions(self, path):
        directions = []
        for i in range(len(path) - 1):
            directions.append((path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]))
        return directions
    
    #returns an array of move directions which represent a path from the start to the end
    def get_path(self, start, end):
        grid = Grid(matrix=self.get_collision_layer())
        start = grid.node(start[0], start[1])
        end = grid.node(end[0], end[1])
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)
        return path

    # Sets the value of the tile at the given location
    def set_layer_id(self, layerName, x, y, value): 
        layer_data = self.layers.get(layerName, [])
        if layer_data and 0 <= x < self.MAPWIDTH and 0 <= y < self.MAPHEIGHT:
            layer_data[y][x] = value

    #returns true if there is a collision at the given location
    def has_collision(self, x, y): 
        collision_id = self.get_layer_id('collision', x, y)
        return collision_id != 0
    
    #returns a list of valid directions to move in
    def get_valid_moves(self, x, y): 
        valid_directions = []
        if y > 0 and not self.has_collision(x, y - 1):
            valid_directions.append((0 , -1))
        if y < self.MAPHEIGHT - 1 and not self.has_collision(x, y + 1):
            valid_directions.append((0 , 1))
        if x > 0 and not self.has_collision(x - 1, y):
            valid_directions.append((-1 , 0))
        if x < self.MAPWIDTH - 1 and not self.has_collision(x + 1, y):
            valid_directions.append((1 , 0))
        return valid_directions
    
    def get_random_valid_move(self, x, y):
        valid_directions = self.get_valid_moves(x, y)
        if len(valid_directions) > 0:
            return valid_directions[random.randint(0, len(valid_directions) - 1)]
        return (0, 0)

    # iterates through all entities and updates them, equal to one step through the game loop
    def update_map(self, entities):
        self.update_layer("sprites", entities)

    # updates the given layer with the given values and positions
    def update_layer(self, layerName, entities):
        #clear layer
        for y in range(self.MAPHEIGHT):
            for x in range(self.MAPWIDTH):
                self.set_layer_id(layerName, x, y, 0)
        for entity in entities:
            self.set_layer_id('sprites', entity.get_component_data('position', 'x'), entity.get_component_data('position', 'y'), entity.get_component_data('render', 'spriteID'))
