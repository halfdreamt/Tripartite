from model.map import Map
from model.entity.entityManager import EntityManager
from model.component.componentManager import ComponentManager
from model.system.systemManager import SystemManager

# The World class is another name for gamestate. It contains the map, the time, and the entities.
class World:
    def __init__(self, masterData):
        # Initialize the map
        self.map = Map()
        self.default_map_data = masterData['map_master']

        self.battle_map_data = {
            "name": "Battle Map",
            "width": 8,
            "height": 5,
            "tilesize": 8,
            "layers": [
                {
                    "name": "Tile Layer 1",
                    "data": [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ]
                }, {
                    "name": "collision",
                    "data": [
                    [157, 158, 158, 158, 158, 158, 158, 159],
                    [181, 0, 0, 0, 0, 0, 0, 183],
                    [181, 0, 0, 0, 0, 0, 0, 183],
                    [181, 0, 0, 0, 0, 0, 0, 183],
                    [205, 206, 206, 206, 206, 206, 206, 207]
                ]
                }, {
                    "name": "sprites",
                    "data": [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 2225, 0, 0, 2221, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ]
                }
            ],
        }

        # Initialize the time
        self.time = 0

        #initialize the systems manager
        self.system_manager = SystemManager()

        # Initialize the component manager
        self.component_manager = ComponentManager(masterData['component_master'], self.system_manager)

        # Initialize the entity manager
        self.entity_manager = EntityManager(masterData['archetype_master'], self.component_manager, self)

        self.initialize_default_map(masterData['map_master'])

    # Iterates through all systems and updates them, equal to one step through the game loop
    def tick(self):
        self.increment_time()
        self.system_manager.update_systems()
        self.map.update_map(self.entity_manager.return_entities())

    def reset_world(self):
        self.initialize_default_map(self.default_map_data)
        self.time = 0
        self.entity_manager.clear_entities()
        spriteData = self.map.get_layer_ids('sprites')
        for sprite in spriteData:
            if sprite[0] == 2225:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2221:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2572:
                self.entity_manager.create_entity('Water Pot',  sprite[0], sprite[1], sprite[2])

    # Increments the time
    def increment_time(self):
        self.time += 1

    def initialize_default_map(self, default_map_data):
        self.map.load_map(default_map_data)
         # Initialize the entities from map data
        spriteData = self.map.get_layer_ids('sprites')
        for sprite in spriteData:
            if sprite[0] == 2225:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2221:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2572:
                self.entity_manager.create_entity('Water Pot',  sprite[0], sprite[1], sprite[2])

    def initialize_battle_map(self):
        self.map.load_map(self.battle_map_data)
        self.time = 0
        self.entity_manager.clear_entities()
        spriteData = self.map.get_layer_ids('sprites')
        for sprite in spriteData:
            if sprite[0] == 2225:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2221:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2572:
                self.entity_manager.create_entity('Water Pot',  sprite[0], sprite[1], sprite[2])
