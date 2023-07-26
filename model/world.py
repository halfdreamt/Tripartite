from model.map import Map
from model.entity.entityManager import EntityManager
from model.component.componentManager import ComponentManager
from model.system.systemManager import SystemManager

# The World class contains time and the entities, including the map entity
class World:
    def __init__(self, masterData):
        # Initialize the map
        self.map = Map()

        self.battle_map = Map()

        # Initialize the time
        self.time = 0

        #initialize the systems manager
        self.system_manager = SystemManager()

        # Initialize the component manager
        self.component_manager = ComponentManager(masterData['component_master'], self.system_manager)

        # Initialize the entity manager
        self.entity_manager = EntityManager(masterData['archetype_master'], self.component_manager, self)

        # Initialize the map entity
        self.entity_manager.create_entity('Map Entity',  0, 0, 0, 'dfghdfg')

        # Initialize the map data
        map_entity = self.entity_manager.get_entities_by_name('Map Entity')
        map_container = map_entity[0].get_component('map_container')
        self.map_data = map_container.get_all_data()
        self.initialize_town_map()
        self.initialize_battle_map()

    # Iterates through all systems and updates them, equal to one step through the game loop
    def tick(self):
        self.increment_time()
        self.system_manager.update_systems()

    def reset_world(self):
        self.time = 0
        self.system_manager.reset_systems()
        self.entity_manager.clear_entities()
        self.initialize_default_map()

    # Increments the time
    def increment_time(self):
        self.time += 1

    def initialize_battle_map(self):
        for map_component in self.map_data['maps']:
            if map_component['data']['name'] == 'Battle Map':
                self.battle_map.load_map(map_component['data'])
                break

    def initialize_town_map(self):
        for map_component in self.map_data['maps']:
            if map_component['data']['name'] == 'Town Map':
                self.map.load_map(map_component['data'])
                break

        self.entity_manager.create_entity('Farmer',  2225, 9, 8, 'defaultMap')
        self.entity_manager.create_entity('Farmer',  2225, 15, 15, 'defaultMap')
        self.entity_manager.create_entity('Water Pot',  2572, 5, 7, 'defaultMap')