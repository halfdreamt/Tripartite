from model.map import Map
from model.entity.entityManager import EntityManager
from model.component.componentManager import ComponentManager
from model.system.systemManager import SystemManager

# The World class is another name for gamestate. It contains the map, the time, and the entities.
class World:
    def __init__(self, map_data, entity_data, component_data):
        # Initialize the map
        self.map = Map(map_data)

        # Initialize the time
        self.time = 0

        #initialize the systems manager
        self.system_manager = SystemManager()

        # Initialize the component manager
        self.component_manager = ComponentManager(component_data, self.system_manager)

        # Initialize the entity manager
        self.entity_manager = EntityManager(entity_data, self.component_manager, self)

        # TODO: don't hardcode this
        # Initialize the entities from map data
        spriteData = self.map.getLayerIds('sprites')
        for sprite in spriteData:
            self.entity_manager.create_entity('Farmer',  sprite[0], sprite[1], sprite[2])

    # Iterates through all systems and updates them, equal to one step through the game loop
    def tick(self):
        self.incrementTime()
        self.system_manager.update_systems()
        self.map.updateMap(self.entity_manager.return_entities())

    # Increments the time
    def incrementTime(self):
        self.time += 1