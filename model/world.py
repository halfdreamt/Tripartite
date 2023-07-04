from model.map import Map
from model.entity.entityManager import EntityManager
from model.component.componentManager import ComponentManager
from model.system.systemManager import SystemManager

# The World class is another name for gamestate. It contains the map, the time, and the entities.
class World:
    def __init__(self, masterData):
        # Initialize the map
        self.map = Map(masterData['map_master'])

        # Initialize the time
        self.time = 0

        #initialize the systems manager
        self.system_manager = SystemManager()

        # Initialize the component manager
        self.component_manager = ComponentManager(masterData['component_master'], self.system_manager)

        # Initialize the entity manager
        self.entity_manager = EntityManager(masterData['archetype_master'], self.component_manager, self)

        # Initialize the entities from map data
        spriteData = self.map.get_layer_ids('sprites')
        for sprite in spriteData:
            if sprite[0] == 2225:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2221:
                self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])
            elif sprite[0] == 2572:
                self.entity_manager.create_entity('Water Pot',  sprite[0], sprite[1], sprite[2])

    # Iterates through all systems and updates them, equal to one step through the game loop
    def tick(self):
        self.increment_time()
        self.system_manager.update_systems()
        self.map.update_map(self.entity_manager.return_entities())

    # Increments the time
    def increment_time(self):
        self.time += 1